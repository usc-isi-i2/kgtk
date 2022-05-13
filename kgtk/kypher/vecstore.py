"""
VectorStore to support Kypher queries over embedding and other vectors.
"""

import os
import os.path
import itertools
import copy

import numpy as np
import h5py

from   kgtk.kypher.utils import *
from   kgtk.exceptions import KGTKException
import kgtk.kypher.indexspec as ispec
from   kgtk.kypher.functions import SqlFunction


### NOTES, TO DO:

# Vector storage:
# - the basic idea is that we use the database or associated file-based storage
#   to store vectors in a parsed, binary format that can then be quickly converted
#   into NumPy format at query time to compute similarities, etc.
# - during import we cut out source vector columns, parse them, and then store
#   the binary data either back in those column as BLOB values ('inline' scheme),
#   or in external NumPy files or HD5 stores.  Other auxiliary values such as
#   precomputed norms, cluster IDs, etc. are also stored in auxiliary columns.  The
#   imported data tables behave like regular KGTK graph tables, the only difference
#   is that vector data has been transformed or offloaded to external stores.
#   The query translator translates column access to appropriate function calls
#   when needed to reconstitute vectors transparently
# - 'inline'- stored data is retrieved directly like other KGTK column values,
#   the only difference is that they are transferred as byte strings which can
#   be very efficiently turned back into NumPy vectors via 'frombuffer' calls
# - externally stored data is stored in NumPy memmap files or HD5 datasets which
#   provide a transparent array interface, in this case vectors are accessed
#   by the 'rowid' of the row from which they were extracted
# - SQLite functions can only accept and return literals and byte strings, we
#   cannot pass arbitrary Python objects such as NumPy vectors.  This works fine
#   for the inline storage scheme, but for external access we have to translate
#   vector accesses into references that can then be converted to vectors by
#   the computations they are passed to (supported by new generalized function API)

# Performance:
# - we (optionally) do load-time vector normalization and store the computed norms
#   in auxiliary columns so we can later denormalize if possible; this allows us
#   to use a simple dot product to compute similarity instead of having to compute
#   the vector norms as well which is somewhat expensive
# - we use the new SQL function definition and translation API to generate vector-column
#   specific translations that have various needed values such as vector data types,
#   data set handles, etc. baked in as call-specific closure variables, so they do
#   not have to be provided or computed when those functions are called.  This keys
#   in on provided call-time arguments to infer what optimizations are possible,
#   generic computation codes cover cases where optimizations aren't possible
# - 'inline' storage is generally the fastest, NumPy provides similar import time
#   and vector access that is about 2x slower.  HD5 also provides similar import
#   time but much slower vector-at-a-time access (40x slower than 'inline')
# - in general, linking vector computations into the inner loop of SQL queries
#   prevents us from using vectorized NumPy operations which are generally faster,
#   but this seems unavoidable without completely changing the DB querying paradigm

# Indexing:
# some pointers that are possibly relevant to creating a FAISS index usable in concert
# with the DB; in particular, we'd only do the clustering, find the relevant cluster(s)
# for each vector, and then do the lookup and vector regeneration ourselves:
# - https://github.com/facebookresearch/faiss/issues/506
# - https://www.pinecone.io/learn/composite-indexes/
# - https://github.com/facebookresearch/faiss/issues/666 (need to use float32 to interface with API)


### VectorStore

class MasterVectorStore(object):
    """Manage auxiliary vector stores to store and access embeddings and other vectors.
    Each individual store manages the vectors of a single KGTK file vector column.
    """

    def __init__(self, store):
        """Create a master vector store for the SQL store 'store'.
        """
        self.store = store
        self.vector_stores = {}

    def close(self):
        for vstore in self.vector_stores.values():
            vstore.close()

    def commit(self):
        for vstore in self.vector_stores.values():
            vstore.commit()

    def get_store_key(self, table, column):
        return (table, column)
    
    def get_store_name(self, table, column):
        return f'{table}:{column}'

    def has_vector_store(self, table, column):
        """Return True if a vector store object for 'table->column' exists, None otherwise.
        """
        return self.vector_stores.get((table, column)) is not None
    
    def get_vector_store(self, table, column, index_spec=None):
        """Return a vector store object for 'table->column'.  If it does not yet exist,
        create it according to 'index_spec' (which must not be None in that case).
        """
        vstore = self.vector_stores.get((table, column))
        if vstore is None:
            if index_spec is None:
                # see if this table column was previously imported with a vector index spec:
                if not self.store.is_vector_column(table, column):
                    raise KGTKException(f'{table}.{column} is not a vector column')
                index_spec = self.store.get_vector_indexes(table)
                index_spec = self.store.normalize_vector_index_specs(table, index_spec)
            if not isinstance(index_spec, ispec.VectorIndex) or not column in index_spec.index.columns:
                raise KGTKException(f'cannot create vector store without valid index spec for {table}.{column}')
            store_type = index_spec.index.columns[column].store
            if store_type == ispec.VectorIndex.STORE_INLINE:
                vstore = InlineVectorStore(self, table, column, index_spec=index_spec)
            elif store_type == ispec.VectorIndex.STORE_NUMPY:
                vstore = NumpyVectorStore(self, table, column, index_spec=index_spec)
            elif store_type == ispec.VectorIndex.STORE_HD5:
                vstore = Hd5VectorStore(self, table, column, index_spec=index_spec)
            else:
                KGTKException(f'unsupported vector store type: {store_type}')
            self.vector_stores[(table, column)] = vstore
        return vstore

    def drop_vector_store_data(self, table, column):
        """If a vector store object for 'table->column' exists, delete any of its data, no-op otherwise.
        """
        if self.has_vector_store(table, column):
            self.get_vector_store(table, column).drop_store_data()

    def get_graph_table_schema(self, table, column, schema):
        """Return a possibly modified version of 'schema' for the graph table containing
        vectors indexed and stored by the vector store for 'table->column'.
        """
        return self.get_vector_store(table, column).get_graph_table_schema(schema)

    def import_vectors(self, table, column, colidx, rows):
        return self.get_vector_store(table, column).import_vectors(colidx, rows)

    @staticmethod
    def get_vector_store_as_array(sql_store, table, column, cache=None):
        master_store = sql_store.get_vector_store()
        # this requires a valid index spec to be available in 'table's graph info:
        vstore = master_store.get_vector_store(table, column)
        ds = vstore.get_store_as_array()
        if cache:
            cache[0] = ds
        return ds

    def vector_column_to_sql(self, table, column, table_alias=None):
        """Return an SQL expression that can be used to generate the actual vectors
        corresponding to the vector-indexed 'column' variable of 'table'.
        """
        return self.get_vector_store(table, column).vector_column_to_sql(table_alias=table_alias)
    
    def vector_column_to_reference_sql(self, table, column, table_alias=None):
        """Return an SQL expression that can be used to access the associated
        vector, using an optimizable vector reference for array-based stores.
        """
        return self.get_vector_store(table, column).vector_column_to_reference_sql(table_alias=table_alias)


class VectorStore(object):
    """Auxiliary vector store to store and access embeddings and other vectors.
    Each individual vector store manages the vectors of a single KGTK file vector column,
    even though multiple stores might share a single physical vector store database (e.g., for HD5).
    """

    def __init__(self, master, table, column, index_spec=None):
        """Create an auxiliary VectorStore for vector column 'table->column' and associate
        it with the master store 'master' and the 'index_spec' describing the store.
        """
        self.master = master
        self.store = master.store
        self.table = table
        self.column = column
        self.index_spec = index_spec
        self.dbfile = None

    def close(self):
        raise KGTKException('not implemented')

    def commit(self):
        raise KGTKException('not implemented')

    def get_store_key(self):
        return self.master.get_store_key(self.table, self.column)
    
    def get_store_name(self):
        return self.master.get_store_name(self.table, self.column)
    
    def drop_store_data(self):
        """If a vector dataset object for 'table->column' exists, delete it, no-op otherwise.
        """
        raise KGTKException('not implemented')

    def get_store_as_array(self):
        """Return an array-like handle that can be used to access the vectors of this store.
        """
        raise KGTKException('not implemented')

    def get_graph_table_schema(self, schema):
        """Return a possibly modified version of 'schema' for the graph table containing
        vectors indexed and stored by this vector store.
        """
        return schema

    def get_vector_format(self):
        return self.index_spec.index.columns[self.column].fmt
            
    def get_vector_dtype(self):
        return np.dtype(self.index_spec.index.columns[self.column].dtype)

    def get_vector_norm(self):
        return self.index_spec.index.columns[self.column].norm
            
    def guess_vector_format(self, example_vector, seps=(' ', ',', ';', ':', '|')):
        """Try to infer an encoding from an 'example_vector'.  For now we only handle
        text strings of numbers separated by one of 'seps' that can be parsed by numpy.
        """
        if not isinstance(example_vector, str):
            raise KGTKException(f"can only handle vectors in text format'")
        example_vector = example_vector.strip()
        for sep in seps:
            if sep in example_vector:
                return 'string', sep
        raise KGTKException(f"unhandled vector format'")

    def parse_vectors(self, vectors, fmt=None, dtype=None):
        fmt = fmt or self.get_vector_format()
        if fmt != ispec.VectorIndex.FORMAT_AUTO:
            raise KGTKException(f"cannot yet handle vector format '{fmt}'")
        dtype = dtype or self.get_vector_dtype()
        vectors = list(vectors)
        if len(vectors) == 0:
            return vectors
        fmt, sep = self.guess_vector_format(vectors[0])
        # parsing text vectors into arrays takes the most time of an import (about the same
        # as uncompressing the data with the gzip library); we tried various other things
        # np.loadtxt, parsing into list to array, json.loads, etc., but to no significant
        # improvement, so we stick with this for now:
        return [np.fromstring(vec, dtype=dtype, sep=sep) for vec in vectors]

    def normalize_vectors(self, vectors):
        """Normalize 'vectors' according to the specified norm and return the normalized
        vectors and a parallel list of norms.
        """
        norm = self.get_vector_norm()
        if norm != ispec.VectorIndex.NORM_L2:
            raise KGTKException(f"cannot handle vector norm '{norm}'")
        # TO DO: see if we are losing too much performance here by not using 2-D array ops:
        norms = [np.linalg.norm(v) for v in vectors]
        vectors = [v / n for v, n in zip(vectors, norms)]
        return vectors, norms

    def import_vectors(self, colidx, rows):
        raise KGTKException('not implemented')

    def vector_column_to_sql(self, table_alias=None):
        """Return an SQL expression that can be used to generate the actual vectors
        corresponding to the vector-indexed 'column' variable of 'table'.
        """
        raise KGTKException('not implemented')
    
    def vector_column_to_reference_sql(self, table_alias=None):
        """Return an SQL expression that can be used to access the associated
        vector, using an optimizable vector reference for array-based stores.
        """
        raise KGTKException('not implemented')


class InlineVectorStore(VectorStore):
    """Auxiliary vector store that stores vectors inline as blob values in SQL rows.
    """

    def __init__(self, master, table, column, index_spec=None):
        """Create an auxiliary VectorStore for vector column 'table->column' and associate
        it with the master store 'master' and the 'index_spec' describing the store.
        """
        super().__init__(master, table, column, index_spec=index_spec)

    def close(self):
        pass

    def commit(self):
        pass

    def drop_store_data(self):
        """If a vector dataset object for 'table->column' exists, delete it, no-op otherwise.
        """
        pass

    def get_graph_table_schema(self, schema):
        """Return a possibly modified version of 'schema' for the graph table containing
        vectors indexed and stored by this vector store.
        """
        schema = copy.deepcopy(schema)
        for column, options in schema.columns.items():
            column = options._name_
            if column == self.column:
                options['type'] = 'BLOB'
                break
        if self.get_vector_norm():
            # append norm column at the end:
            norm_column = f'{self.column};_kgtk_vec_norm'
            # TO DO: if we use FLOAT here, we get back bytes, figure out why:
            schema.columns[norm_column] = sdict['_name_': norm_column, 'type': 'TEXT']
        return schema

    def import_vectors(self, colidx, rows):
        """Parse a collection of source vectors stored at 'rows[colidx]' into a two-dimensional
        numpy array of vectors, and incrementally add them to this vector store.
        """
        source_vectors = map(lambda row: row[colidx], rows)
        vectors = self.parse_vectors(source_vectors)
        if len(vectors) == 0:
            return rows
        norms = None
        if self.get_vector_norm():
            vectors, norms = self.normalize_vectors(vectors)
        vectors = map(lambda v: v.tobytes(), vectors)
        any(itertools.filterfalse(lambda row: not row.__setitem__(colidx, next(vectors)), rows))
        if norms is not None:
            # append stringified norms to the end of each row - figure out why we can't use floats:
            norms = iter(norms)
            any(itertools.filterfalse(lambda row: not row.append(str(next(norms))), rows))
        return rows

    def vector_column_to_sql(self, table_alias=None):
        """Return an SQL expression that can be used to generate the actual vectors
        corresponding to the vector-indexed 'column' variable of 'table'.
        """
        table = table_alias or self.table
        return f'{table}.{self.column}'

    def vector_column_to_reference_sql(self, table_alias=None):
        """Return an SQL expression that can be used to access the associated
        vector, using an optimizable vector reference for array-based stores.
        """
        return self.vector_column_to_sql(table_alias=table_alias)


# NumPy memmap notes:
# - see: https://numpy.org/devdocs/reference/generated/numpy.lib.format.html
# - this is significantly faster than the HD5 access (goes from 2.5 to 0.68 secs for 10k vecs)
# - further speedups down to 0.16 secs possible with vector norm precomputation
#   (see .work/embeddings-precompute-norms.log - note that the dot-product cost for this
#   is 0.015 secs, so we have another factor 10 head room for speeding up vector access)
# - np.frombuffer is really fast, 10M calls to generate a 100d array from bytes takes 4.25 secs
#   ( x = np.frombuffer(bytes, dtype=np.float32) ), so storing the bytes on the DB as 
#   binary blobs might be the best thing after all (about 20secs for 10M vectors with precomputed norms)
# - np.frombuffer takes an offset, so we could encode a norm as the first element and
#   read from an offset to skip it (but we now store the norms separately for a simpler format)
# - we could use the struct package to get a norm value encoded in the first 4 bytes:
#   - fmt=struct.Struct('<f'), fmt.unpack(vbytes[0:4]) -> (-0.10274789482355118,)

class NumpyVectorStore(VectorStore):
    """Auxiliary vector store that stores vectors via numpy memmaps.
    """

    def __init__(self, master, table, column, index_spec=None):
        """Create an auxiliary VectorStore for vector column 'table->column' and associate
        it with the master store 'master' and the 'index_spec' describing the store.
        """
        super().__init__(master, table, column, index_spec=index_spec)
        self.dbfile = None
        self.conn = None

    def get_store_dbfile(self):
        if self.dbfile is None:
            vsname = self.get_store_name()
            self.dbfile = f'{self.store.dbfile}.vec.{vsname}.npy'
        return self.dbfile

    def get_store_conn(self, mode='r', mmap=False):
        """Return the dataset file connection object for this dataset, open it if necessary
        according to 'mode'.  If it is already open in read mode but a write-mode is
        requested, close it and reopen it according to the new mode (unless the underlying
        SQL store is in read-only mode).
        """
        conn = self.conn
        if conn is None:
            dbfile = self.get_store_dbfile()
            if self.store.readonly:
                # ignore mode, always open as read-only:
                mode = 'r'
            elif not os.path.exists(dbfile):
                # create an empty .npy file so we can open it with any mode, we'll fix up info later:
                np.save(dbfile, np.zeros(0))
            if mmap:
                conn = np.load(dbfile, mmap_mode='r', fix_imports=False)
            else:
                mode += 'b' if 'b' not in mode else ''
                conn = open(dbfile, mode)
            self.conn = conn
        elif mode != 'r' and conn.mode == 'r' and not isinstance(conn, np.memmap) and not self.store.readonly:
            # regular file opened as read-only, close and reopen with provided write mode:
            conn.close()
            conn = open(dbfile, mode)
            self.conn = conn
        return conn

    def get_store_as_array(self):
        """Return an array-like handle that can be used to access the vectors of this store.
        """
        return self.get_store_conn(mode='r', mmap=True)

    def update_dataset_header(self, ds, ndim=None, dtype=None):
        dtype = dtype or self.get_vector_dtype()
        curpos = ds.tell()
        ds.seek(0)
        version1 = np.lib.format.read_magic(ds)[0] == 1
        if version1:
            shape, fo, dt = np.lib.format.read_array_header_1_0(ds)
        else:
            shape, fo, dt = np.lib.format.read_array_header_2_0(ds)
        startpos = ds.tell()
        if shape[0] == 0:
            if ndim is None:
                raise KGTKException(f"cannot determine ndim of vector dataset")
        else:
            _, ndim = shape
        ds.seek(0, 2)
        endpos = ds.tell()
        dtype = np.dtype(dtype)
        nbytes = dtype.itemsize
        count = (endpos - startpos) // (ndim * nbytes)
        desc = {'descr': np.lib.format.dtype_to_descr(dtype), 'fortran_order': fo, 'shape': (count, ndim)}
        ds.seek(0)
        if version1:
            np.lib.format.write_array_header_1_0(ds, desc)
        else:
            np.lib.format.write_array_header_2_0(ds, desc)
        ds.seek(curpos)

    def close(self):
        if self.conn is not None:
            if not isinstance(self.conn, np.memmap):
                self.conn.close()
        self.conn = None

    def commit(self):
        self.close()

    def drop_store_data(self):
        """If a vector dataset object for 'table->column' exists, delete it, no-op otherwise.
        """
        self.close()
        dbfile = self.get_store_dbfile()
        if os.path.exists(dbfile):
            os.remove(dbfile)

    def get_graph_table_schema(self, schema):
        """Return a possibly modified version of 'schema' for the graph table containing
        vectors indexed and stored by this vector store.
        """
        schema = copy.deepcopy(schema)
        if self.get_vector_norm():
            # append norm column at the end:
            norm_column = f'{self.column};_kgtk_vec_norm'
            # TO DO: if we use FLOAT here, we get back bytes, figure out why:
            schema.columns[norm_column] = sdict['_name_': norm_column, 'type': 'TEXT']
        return schema
    
    def import_vectors(self, colidx, rows):
        """Parse a collection of source vectors stored at 'rows[colidx]' into a two-dimensional
        numpy array of vectors, and incrementally add them to this vector store.
        """
        source_vectors = map(lambda row: row[colidx], rows)
        vectors = self.parse_vectors(source_vectors)
        if len(vectors) == 0:
            return rows
        ds = self.conn
        if ds is None or 'a' not in ds.mode:
            # maybe use a 'create_dataset' here for a cleaner API
            # (we do need 'r+' here so we can append and read/write the header):
            ds = self.get_store_conn(mode='r+')
            # a+ doesn't do what we want, so we have to position by hand:
            ds.seek(0, 2)
        norms = None
        if self.get_vector_norm():
            vectors, norms = self.normalize_vectors(vectors)
        # writing the whole chunk in a single write op doesn't save us anything:
        for vec in vectors:
            ds.write(vec.tobytes())
        self.update_dataset_header(ds, ndim=len(vectors[0]))
        # set all the respective fields in the KGTK source file tuples to the empty value:
        any(itertools.filterfalse(lambda row: not row.__setitem__(colidx, ''), rows))
        if norms is not None:
            # append stringified norms to the end of each row - figure out why we can't use floats:
            norms = iter(norms)
            any(itertools.filterfalse(lambda row: not row.append(str(next(norms))), rows))
        return rows

    def vector_column_to_sql(self, table_alias=None):
        """Return an SQL expression that can be used to generate the actual vectors
        corresponding to the vector-indexed 'column' variable of 'table'.
        """
        vfn = SqlFunction.get_function('_kvec_get_vector', store=self.store, uniq=True, xstore=self)
        vfn.load()
        table = table_alias or self.table
        return f'{vfn.get_name()}({table}.rowid)'

    def vector_column_to_reference_sql(self, table_alias=None):
        """Return an SQL expression that can be used to access the associated
        vector, using an optimizable vector reference for array-based stores.
        """
        table = table_alias or self.table
        # NOTE: rowid is 1-based
        return f'{table}.rowid'


class Hd5VectorStore(VectorStore):
    """Auxiliary vector store to store and access embeddings and other vectors.
    """

    def __init__(self, master, table, column, index_spec=None):
        """Create an auxiliary VectorStore for vector column 'table->column' and associate
        it with the master store 'master' and the 'index_spec' describing the store.
        """
        super().__init__(master, table, column, index_spec=index_spec)
        # a vector cache is tightly linked to its parent SQL store, so we use a fixed pattern here:
        self.dbfile = self.store.dbfile + '.vec.hdf5'
        self.conn = None

    def get_linked_stores(self):
        # all HD5 stores of this master store share a single DB file and connection:
        return [vstore for vstore in self.master.vector_stores.values() if isinstance(vstore, Hd5VectorStore)]

    def get_conn(self, mode='r'):
        """Return the HD5 file connection object for this store, open it if necessary
        according to 'mode'.  If it is already open in read mode but a write-mode is
        requested, close it and reopen it according to the new mode (unless the underlying
        SQL store is in read-only mode).  We only upgrade the mode from 'r' to 'r+' if
        needed, we never go the other direction.
        """
        if self.conn is None:
            for vstore in self.get_linked_stores():
                if vstore.conn is not None:
                    self.conn = vstore.conn
                    break
        if self.conn is None:
            if self.store.readonly:
                # ignore mode, always open as read-only:
                mode = 'r'
            elif mode == 'r' and not os.path.exists(self.dbfile):
                # create the file so we can open it with 'r':
                h5py.File(self.dbfile, 'a').close()
            self.conn = h5py.File(self.dbfile, mode)
        elif mode != 'r' and self.conn.mode == 'r' and not self.store.readonly:
            # opened as read-only, close and reopen with provided write mode:
            self.close()
            self.conn = h5py.File(self.dbfile, mode)
        return self.conn

    def close(self):
        for vstore in self.get_linked_stores():
            if vstore.conn is not None:
                vstore.conn.close()
            vstore.conn = None

    def commit(self):
        self.close()

    def get_store_dataset(self):
        """Return a vector dataset object for 'table->column' if it exists, None otherwise.
        """
        return self.get_conn().get(self.get_store_name())

    def get_store_as_array(self):
        """Return an array-like handle that can be used to access the vectors of this store.
        """
        return self.get_store_dataset()

    def drop_store_data(self):
        """If a vector dataset object for 'table->column' exists, delete it, no-op otherwise.
        """
        ds = self.get_store_dataset()
        if ds is not None:
            del self.get_conn(mode='r+')[self.get_store_name()]

    def get_graph_table_schema(self, schema):
        """Return a possibly modified version of 'schema' for the graph table containing
        vectors indexed and stored by this vector store.
        """
        schema = copy.deepcopy(schema)
        if self.get_vector_norm():
            # append norm column at the end:
            norm_column = f'{self.column};_kgtk_vec_norm'
            # TO DO: if we use FLOAT here, we get back bytes, figure out why:
            schema.columns[norm_column] = sdict['_name_': norm_column, 'type': 'TEXT']
        return schema
    
    def import_vectors(self, colidx, rows):
        """Parse a collection of source vectors stored at 'rows[colidx]' into a two-dimensional
        numpy array of vectors, and incrementally add them to this vector store.
        """
        source_vectors = map(lambda row: row[colidx], rows)
        vectors = self.parse_vectors(source_vectors)
        if len(vectors) == 0:
            return rows
        ds = self.get_store_dataset()
        if ds is None:
            dsname = self.get_store_name()
            ndim = len(vectors[0])
            dtype = self.get_vector_dtype()
            chunksize = self.store.VECTOR_IMPORT_CHUNKSIZE
            conn = self.get_conn(mode='r+')
            # we need chunking so we can resize, otherwise we'd have to know the number of vectors ahead of time;
            # we use auto-chunking for now, but maybe supplying an explicit shape would be better:
            ds = conn.create_dataset(dsname, dtype=dtype, shape=(0,ndim), maxshape=(None,ndim), chunks=True)
        norms = None
        if self.get_vector_norm():
            vectors, norms = self.normalize_vectors(vectors)
        size, ndim = ds.shape
        ds.resize(size + len(vectors), axis=0)
        ds[size:] = vectors
        # set all the respective fields in the KGTK source file tuples to the empty value:
        any(itertools.filterfalse(lambda row: not row.__setitem__(colidx, ''), rows))
        if norms is not None:
            # append stringified norms to the end of each row - figure out why we can't use floats:
            norms = iter(norms)
            any(itertools.filterfalse(lambda row: not row.append(str(next(norms))), rows))
        return rows

    def vector_column_to_sql(self, table_alias=None):
        """Return an SQL expression that can be used to generate the actual vectors
        corresponding to the vector-indexed 'column' variable for 'self.table'.
        """
        vfn = SqlFunction.get_function('_kvec_get_vector', store=self.store, xstore=self)
        vfn.load()
        table = table_alias or self.table
        return f'{vfn.get_name()}({table}.rowid)'

    def vector_column_to_reference_sql(self, table_alias=None):
        """Return an SQL expression that can be used to access the associated
        vector, using an optimizable vector reference for array-based stores.
        """
        table = table_alias or self.table
        # NOTE: rowid is 1-based
        return f'{table}.rowid'
