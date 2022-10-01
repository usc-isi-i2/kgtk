"""
VectorStore to support Kypher queries over embedding and other vectors.
"""

import sys
import os
import os.path
import itertools
import copy
import math
from   functools import lru_cache

import numpy as np
import h5py
import faiss

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
        # strip off any DB prefixes if necessary:
        _, table = self.store.parse_table_name(table)
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
        if vstore is not None and vstore.index_spec != index_spec and index_spec is not None:
            # redefinition with a different index spec, replace the old one:
            vstore = None
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
        """Return an array-like handle that can be used to access the vectors of
        the vector store for 'table->column'.  'cache' can be used to cache the
        array object in SQL vector functions for fast repeated access.
        """
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
        self.vector_ndim = None
        self.vector_dtype = None
        self.vector_norm = None
        self.ntotal = None
        self.nn_index = None

    def close(self):
        raise KGTKException('not implemented')

    def commit(self):
        raise KGTKException('not implemented')

    def get_store_key(self):
        return self.master.get_store_key(self.table, self.column)
    
    def get_store_name(self):
        return self.master.get_store_name(self.table, self.column)

    def get_sqlstore_dbfile(self):
        """Return the DB file in which the data for 'self.table' resides.
        """
        return self.store.get_table_dbfile(self.table)
    
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

    def get_norm_column_name(self):
        return f'{self.column};_kgtk_vec_norm'

    def get_quantizer_cell_column_name(self):
        return f'{self.column};_kgtk_vec_qcell'
    
    def get_vector_index_options(self):
        """Return the full options dict for the index spec of this store.
        """
        return self.index_spec.index.columns[self.column]

    def get_vector_format(self):
        return self.index_spec.index.columns[self.column].fmt
            
    def get_vector_dtype(self):
        if self.vector_dtype is None:
            self.vector_dtype = np.dtype(self.index_spec.index.columns[self.column].dtype)
        return self.vector_dtype

    def get_vector_norm(self):
        if self.vector_norm is None:
            normspec = self.index_spec.index.columns[self.column].norm
            # since we now have NN-indexes, we only normalize if explicitly requested:
            if normspec is True:
                # if just True was explicitly specified, use this as the default:
                normspec = ispec.VectorIndex.NORM_L2
            self.vector_norm = normspec
        return self.vector_norm

    def get_vector_ndim(self):
        raise KGTKException('not implemented')
            
    def get_store_ntotal(self):
        """Return the total number of vectors stored in this store.
        """
        raise KGTKException('not implemented')

    def guess_vector_format(self, example_vector, seps=(',', ';', ':', '|', ' ')):
        """Try to infer an encoding from an 'example_vector'.  For now we only handle
        text strings of numbers separated by one of 'seps' that can be parsed by numpy.
        NOTE: white space separators need to be listed AFTER any others so that
        separators followed by whitespace will be handled correctly.
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

    def get_vectors_as_array(self, n, offset=0, buffer=None):
        """Return 'n' contiguous vectors of this store starting at 'offset'.
        If 'buffer is supplied, copy the vectors into it (assuming it is big enough and of the right type).
        Return the array of vectors and the number of vectors returned in it.
        """
        raise KGTKException('not implemented')
    
    def get_qcell_vectors(self, qcell):
        """Return all vectors assigned to this quantizer 'qcell' as an array.
        Return their zero-based rowid's as a second array of vector IDs.
        """
        raise KGTKException('not implemented')

    def get_vector_rows_by_id(self, ids):
        """Retrieve vector rows based on a single or collection of zero-based vector row 'ids'.
        Each returned tuple contains the 'id', 'node1', 'label', vector-id and respective vector
        of that row.  Any additional relevant columns such as norm, qcell,  etc. will also be
        returned if they are defined.
        """
        if isinstance(ids, (int, str)):
            ids = [ids]
        
        # NOTE:  DB 'rowid's are 1-based
        # TO DO: construct and cache this query, instead of redoing this every time:
        normcol = f', {sql_quote_ident(self.get_norm_column_name())}' if self.get_vector_norm() else ''
        qcellcol = self.get_quantizer_cell_column_name()
        qcellcol = f', {sql_quote_ident(qcellcol)}' if self.store.has_table_column(self.table, qcellcol) else ''
        query = f"""
            SELECT id, node1, label, {self.table}.rowid-1, {sql_quote_ident(self.column)} {normcol} {qcellcol}
            FROM {self.table}
            WHERE {self.table}.rowid = ?"""

        # this is a super-method which doesn't actually fill in vector objects, those are added below:
        # TO DO: possibly batch this instead of going id-by-id, but for now this is just used to
        # retrieve small batches of top-k results, so batching is not an issue
        rows = []
        for id in ids:
            rows += [list(row) for row in self.store.execute(query, (int(id)+1,))]
        return rows

    def get_nearest_neighbor_index(self):
        """Return an appropriate nearest neighbor index object for this store if one has been configured,
        return False otherwise.
        """
        if self.nn_index is None:
            self.nn_index = self.index_spec.index.columns[self.column].nn
            if self.nn_index:
                # for now this is all we support:
                self.nn_index = FaissIndex(self)
        return self.nn_index


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
            norm_column = self.get_norm_column_name()
            # TO DO: if we use FLOAT here, we get back bytes, figure out why:
            schema.columns[norm_column] = sdict['_name_': norm_column, 'type': 'TEXT']
        return schema

    def get_vector_ndim(self):
        if self.vector_ndim is None:
            # for now, infer it from the first row in the table, but maybe we need to store it somewhere explicitly:
            for (vec,) in self.store.execute(f'SELECT {sql_quote_ident(self.column)} FROM {self.table} LIMIT 1'):
                self.vector_ndim = len(np.frombuffer(vec, dtype=self.get_vector_dtype()))
        return self.vector_ndim

    def get_store_ntotal(self):
        """Return the total number of vectors stored in this store.
        """
        if self.ntotal is None:
            # for now, infer it from the size of the table, but maybe we need to store it somewhere explicitly:
            self.ntotal = self.store.get_table_row_count(self.table)
        return self.ntotal

    def import_vectors(self, colidx, rows):
        """Parse a collection of source vectors stored at 'rows[colidx]' into a two-dimensional
        numpy array of vectors, and incrementally add them to this vector store.
        """
        source_vectors = map(lambda row: row[colidx], rows)
        vectors = self.parse_vectors(source_vectors)
        if len(vectors) == 0:
            return rows
        # update these values dynamically during import:
        if self.vector_ndim is None:
            self.vector_ndim = len(vectors[0])
            self.ntotal = len(vectors)
        else:
            self.ntotal += len(vectors)
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
        return f'{table}.{sql_quote_ident(self.column)}'

    def vector_column_to_reference_sql(self, table_alias=None):
        """Return an SQL expression that can be used to access the associated
        vector, using an optimizable vector reference for array-based stores.
        """
        return self.vector_column_to_sql(table_alias=table_alias)
    
    def get_vectors_as_array(self, n, offset=0, buffer=None):
        """Return 'n' contiguous vectors of this store starting at 'offset'.
        If 'buffer is supplied, copy the vectors into it (assuming it is big enough and of the right type).
        Return the array of vectors and the number of vectors returned in it.
        """
        # NOTE: if a buffer is supplied, float type conversions will happen automatically
        ntotal = self.get_store_ntotal()
        end = min(offset + n, ntotal)
        nvecs = end - offset
        dtype = self.get_vector_dtype()
        if buffer is None:
            # allocate it for size=n, even if nvecs is smaller than that:
            ndim = self.get_vector_ndim()
            buffer = np.zeros(n * ndim, dtype=dtype)
            buffer.shape = (n, ndim)
        # note that 'rowid's are 1-based:
        for i, (vec,) in enumerate(self.store.execute(f"""
            SELECT {sql_quote_ident(self.column)} FROM {self.table}
            WHERE {self.table}.rowid >= ?
            LIMIT ?""", (offset + 1, n))):
            buffer[i] = np.frombuffer(vec, dtype=dtype)
        return buffer, nvecs

    # NOTE: 50 qcells with 16K 1K-D vectors each take up about 3GB of RAM:
    @lru_cache(maxsize=50)
    def get_qcell_vectors(self, qcell):
        """Return all vectors assigned to this quantizer 'qcell' as an array.
        Return their zero-based rowid's as a second array of vector IDs.
        """
        dtype = self.get_vector_dtype()
        qcell_colname = self.get_quantizer_cell_column_name()
        vectors = []
        vectorids = []
        # NOTE: DB 'rowid's are 1-based
        # PERFORMANCE NOTE: the speed of this query greatly depends on how contiguous rows
        # with this 'qcell' ID are on disk, so sorting by qcell-ID speeds things up a lot
        for vec, vecid in self.store.execute(f"""
            SELECT {sql_quote_ident(self.column)}, {self.table}.rowid FROM {self.table}
            WHERE {self.table}.{sql_quote_ident(qcell_colname)} = ?""", (str(qcell),)):
            vectors.append(np.frombuffer(vec, dtype=dtype))
            vectorids.append(int(vecid)-1)
        if len(vectors) > 0:
            return np.vstack(vectors), np.array(vectorids, dtype=np.int64)
        else:
            return np.zeros(0, dtype=dtype), np.zeros(0, dtype=np.int64)

    def get_vector_rows_by_id(self, ids):
        """Retrieve vector rows based on a single or collection of zero-based vector row 'ids'.
        Each returned tuple contains the 'id', 'node1', 'label', vector-id and respective vector
        of that row.  Any additional relevant columns such as norm, qcell,  etc. will also be
        returned if they are defined.
        """
        rows = super().get_vector_rows_by_id(ids)
        dtype = self.get_vector_dtype()
        for row in rows:
            row[4] = np.frombuffer(row[4], dtype=dtype)
        return rows


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
        self.external_dbfile = None
        self.conn = None

    def get_store_dbfile(self):
        if self.dbfile is None:
            self.dbfile = self.get_store_external_file()
            if self.dbfile is None:
                vsname = self.get_store_name()
                self.dbfile = f'{self.get_sqlstore_dbfile()}.vec.{vsname}.npy'
        return self.dbfile

    def has_external_file(self):
        """Return True if this store is defined by an external .npy file.
        """
        if self.dbfile is None:
            self.dbfile = self.get_store_external_file()
        return self.external_dbfile is not None

    def get_store_conn(self, mode='r', mmap=False):
        """Return the dataset file connection object for this dataset, open it if necessary
        according to 'mode'.  If it is already open in read mode but a write-mode is
        requested, close it and reopen it according to the new mode (unless the underlying
        SQL store is in read-only mode).
        """
        conn = self.conn
        if conn is None:
            dbfile = self.get_store_dbfile()
            if self.store.readonly or self.has_external_file():
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

    def read_dataset_header(self, dsspec):
        try:
            if isinstance(dsspec, str):
                ds = open(dsspec, 'rb')
            else:
                ds = dsspec
            ds.seek(0)
            version = np.lib.format.read_magic(ds)[0]
            if version == 1:
                shape, fo, dt = np.lib.format.read_array_header_1_0(ds)
            else:
                shape, fo, dt = np.lib.format.read_array_header_2_0(ds)
            return shape, fo, dt, version
        finally:
            if isinstance(dsspec, str):
                ds.close()

    def update_dataset_header(self, ds, ndim=None, dtype=None):
        dtype = dtype or self.get_vector_dtype()
        curpos = ds.tell()
        shape, fo, dt, version = self.read_dataset_header(ds)
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
        if version == 1:
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
        if not self.has_external_file() and os.path.exists(dbfile):
            os.remove(dbfile)

    def get_graph_table_schema(self, schema):
        """Return a possibly modified version of 'schema' for the graph table containing
        vectors indexed and stored by this vector store.
        """
        schema = copy.deepcopy(schema)
        if self.get_vector_norm() and not self.has_external_file():
            # append norm column at the end:
            norm_column = self.get_norm_column_name()
            # TO DO: if we use FLOAT here, we get back bytes, figure out why:
            schema.columns[norm_column] = sdict['_name_': norm_column, 'type': 'TEXT']
        return schema

    def get_vector_ndim(self):
        if self.vector_ndim is None:
            dbfile = self.get_store_dbfile()
            shape, fo, dt, version = self.read_dataset_header(dbfile)
            if shape[0] == 0:
                raise KGTKException(f"cannot determine shape of vector dataset")
            self.ntotal = shape[0]
            self.vector_ndim = shape[1]
        return self.vector_ndim

    def get_vector_norm(self):
        if self.vector_norm is None:
            if self.has_external_file() and self.index_spec.index.columns[self.column].norm is None:
                # this is different than the default behavior if we have an external store file,
                # in which case we use False as the default if the user didn't specify anything,
                # since we can't normalize the vectors on the external file; however, we still
                # want to be able to indicate normalization if the external vectors are normalized:
                self.vector_norm = False
            else:
                return super().get_vector_norm()
        return self.vector_norm

    def get_store_ntotal(self):
        """Return the total number of vectors stored in this store.
        """
        if self.ntotal is None:
            # this will assign it as a side-effect:
            self.get_vector_ndim()
        return self.ntotal

    def get_store_external_file(self):
        if self.dbfile is None:
            self.external_dbfile = self.index_spec.index.columns[self.column].ext
            self.dbfile = self.external_dbfile
            if self.dbfile is not None:
                shape, fo, dt, version = self.read_dataset_header(self.dbfile)
                # TO DO: maybe check for mismatches from the index spec, for now
                # we simply accept whatever comes with the external NumPy file:
                self.ntotal = shape[0]
                self.vector_ndim = shape[1]
                self.dtype = np.dtype(dt)
        return self.dbfile
    
    def import_vectors(self, colidx, rows):
        """Parse a collection of source vectors stored at 'rows[colidx]' into a two-dimensional
        numpy array of vectors, and incrementally add them to this vector store.
        """
        if self.has_external_file():
            # no import required, but just in case, still set the vector column fields to '':
            any(itertools.filterfalse(lambda row: not row.__setitem__(colidx, ''), rows))
            return rows
        # parse and import the vectors:
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

    def get_vectors_as_array(self, n, offset=0, buffer=None):
        """Return 'n' contiguous vectors of this store starting at 'offset'.
        If 'buffer is supplied, copy the vectors into it (assuming it is big enough and of the right type).
        Return the array of vectors and the number of vectors returned in it.
        """
        # NOTE: if a buffer is supplied, float type conversions will happen automatically
        ntotal = self.get_store_ntotal()
        end = min(offset + n, ntotal)
        nvecs = end - offset
        if buffer is not None:
            # caller must ensure that buffer is large enough:
            buffer[0:nvecs] = self.get_store_as_array()[offset:end]
            return buffer, nvecs
        else:
            return self.get_store_as_array()[offset:end], nvecs

    @lru_cache(maxsize=50)
    def get_qcell_vectors(self, qcell):
        """Return all vectors assigned to this quantizer 'qcell' as an array.
        Return their zero-based rowid's as a second array of vector IDs.
        """
        dtype = self.get_vector_dtype()
        qcell_colname = self.get_quantizer_cell_column_name()
        store_vectors = self.get_store_as_array()
        vectors = []
        vectorids = []
        # NOTE: 'rowid's are 1-based
        # PERFORMANCE NOTE: the speed of this query greatly depends on how contiguous rows
        # with this 'qcell' ID are on disk, so sorting by qcell-ID speeds things up a lot
        for (vecid,) in self.store.execute(f"""
            SELECT {self.table}.rowid FROM {self.table}
            WHERE {self.table}.{sql_quote_ident(qcell_colname)} = ?""", (str(qcell),)):
            vecid = int(vecid)-1
            vectors.append(store_vectors[vecid])
            vectorids.append(vecid)
        if len(vectors) > 0:
            return np.vstack(vectors), np.array(vectorids, dtype=np.int64)
        else:
            return np.zeros(0, dtype=dtype), np.zeros(0, dtype=np.int64)

    def get_vector_rows_by_id(self, ids):
        """Retrieve vector rows based on a single or collection of zero-based vector row 'ids'.
        Each returned tuple contains the 'id', 'node1', 'label', vector-id and respective vector
        of that row.  Any additional relevant columns such as norm, qcell,  etc. will also be
        returned if they are defined.
        """
        rows = super().get_vector_rows_by_id(ids)
        store_vectors = self.get_store_as_array()
        for row in rows:
            row[4] = store_vectors[row[3]]
        return rows


class Hd5VectorStore(VectorStore):
    """Auxiliary vector store to store and access embeddings and other vectors.
    """

    def __init__(self, master, table, column, index_spec=None):
        """Create an auxiliary VectorStore for vector column 'table->column' and associate
        it with the master store 'master' and the 'index_spec' describing the store.
        """
        super().__init__(master, table, column, index_spec=index_spec)
        # a vector cache is tightly linked to its parent SQL store, so we use a fixed pattern here:
        self.dbfile = self.get_sqlstore_dbfile() + '.vec.hdf5'
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
            norm_column = self.get_norm_column_name()
            # TO DO: if we use FLOAT here, we get back bytes, figure out why:
            schema.columns[norm_column] = sdict['_name_': norm_column, 'type': 'TEXT']
        return schema

    def get_vector_ndim(self):
        if self.vector_ndim is None:
            self.ntotal, self.vector_ndim = self.get_store_as_array().shape
        return self.vector_ndim
    
    def get_store_ntotal(self):
        """Return the total number of vectors stored in this store.
        """
        if self.ntotal is None:
            # this will assign it as a side-effect:
            self.get_vector_ndim()
        return self.ntotal

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

    def get_vectors_as_array(self, n, offset=0, buffer=None):
        """Return 'n' contiguous vectors of this store starting at 'offset'.
        If 'buffer is supplied, copy the vectors into it (assuming it is big enough and of the right type).
        Return the array of vectors and the number of vectors returned in it.
        """
        # NOTE: if a buffer is supplied, float type conversions will happen automatically
        ntotal = self.get_store_ntotal()
        end = min(offset + n, ntotal)
        nvecs = end - offset
        if buffer is not None:
            # caller must ensure that buffer is large enough:
            buffer[0:nvecs] = self.get_store_as_array()[offset:end]
            return buffer, nvecs
        else:
            return self.get_store_as_array()[offset:end], nvecs

    @lru_cache(maxsize=50)
    def get_qcell_vectors(self, qcell):
        """Return all vectors assigned to this quantizer 'qcell' as an array.
        Return their zero-based rowid's as a second array of vector IDs.
        """
        dtype = self.get_vector_dtype()
        qcell_colname = self.get_quantizer_cell_column_name()
        store_vectors = self.get_store_as_array()
        vectors = []
        vectorids = []
        # NOTE: 'rowid's are 1-based
        # PERFORMANCE NOTE: the speed of this query greatly depends on how contiguous rows
        # with this 'qcell' ID are on disk, so sorting by qcell-ID speeds things up a lot
        for (vecid,) in self.store.execute(f"""
            SELECT {self.table}.rowid FROM {self.table}
            WHERE {self.table}.{sql_quote_ident(qcell_colname)} = ?""", (str(qcell),)):
            vecid = int(vecid)-1
            vectors.append(store_vectors[vecid])
            vectorids.append(vecid)
        if len(vectors) > 0:
            return np.vstack(vectors), np.array(vectorids, dtype=np.int64)
        else:
            return np.zeros(0, dtype=dtype), np.zeros(0, dtype=np.int64)

    def get_vector_rows_by_id(self, ids):
        """Retrieve vector rows based on a single or collection of zero-based vector row 'ids'.
        Each returned tuple contains the 'id', 'node1', 'label', vector-id and respective vector
        of that row.  Any additional relevant columns such as norm, qcell,  etc. will also be
        returned if they are defined.
        """
        rows = super().get_vector_rows_by_id(ids)
        store_vectors = self.get_store_as_array()
        for row in rows:
            row[4] = store_vectors[row[3]]
        return rows


### Indexing:

# Metric notes:
# - from https://github.com/facebookresearch/faiss/blob/main/faiss/MetricType.h:
#     Most algorithms support both inner product and L2, with the flat
#     (brute-force) indices supporting additional metric types for vector comparison
#
#     faiss.METRIC_INNER_PRODUCT = 0   # maximum inner product search
#     faiss.METRIC_L2 = 1              # squared L2 search
#     faiss.METRIC_L1                  # L1 (aka cityblock), Manhattan-distance
#
# - stored in 'index.metric_type'
# - for Kmeans the default is squared L2 (so we don't need sqrt)
# - inner product is supported, but that might be potentially bad for quantization,
#   since now all vectors are mapped onto a unit circle (think about that)
#
# Indexing notes:
# - clustering.train method takes init centroids as a parameter, so training
#   on smaller batches of data is possible by restaring with the clusters
#   from the prior batch
#   - see https://github.com/facebookresearch/faiss/issues/531
# - see this for details on index factory:
#   https://github.com/facebookresearch/faiss/wiki/The-index-factory
#   https://gist.github.com/mdouze/c3111d5f12d1308f5adf78dcd48cdf37  (factory_string.bnf)
#   https://github.com/facebookresearch/faiss/blob/main/faiss/index_factory.cpp
# - we might be able to use faiss.IndexShards to search over multiple shards in parallel
#
# Scaling, sampling, dimensioning:
# - FAISS requires 39 min_points_per_centroid for training (otherwise warning),
#   and subsamples data if we have more than 256 max_points_per_centroid, so
#   we should mirror / approximate that when we read training data from the DB
# - to allow training on data where the required sample does not fit into RAM
#   we can use two basic approaches:
#   (1) train an index an iteration at a time where at each iteration we provide
#       a different window on the training sample that can be loaded into RAM.
#       This seems to work, a sliding window can also be used but might not help.
#       The advantage of this that we end up with a single quantizer for all
#       of the data which makes access simpler.
#   (2) train indexes on subsections of the data whose training sample fits into RAM;
#       then search on all of those during query time and combine results, or
#       use a faiss.IndexShards that does the combined searching for us.  We
#       kind of figured out how to do that, there are still a couple of wrinkles
#       to iron out.  The advantage of that is that the training of the shards
#       is on complete data slices, and that the querying is automatically threaded.
# - either way, given a max-RAM target and a set of vectors, we can compute whether
#   we need one or more training slices, and whether they need to be subsampled
# - Example situations:
#   - 55M 100d vectors, 8K vectors per centroid, 8GB of RAM
#     need 6714 centroids, pick 8192 (next power of 2),
#     min-train = 39*8192 = 319488, avg-train = 128*8192 = 1048576, max-train = 2097152,
#     min-RAM = 121MB, max-RAM = 800MB; no batching/sharding needed, train in single run,
#     even if we go to 1K vectors per centroid, we need at most 6.5GB or so
#   - 100M 1024d vectors, 1K vectors per centroid, 16GB of RAM
#     need 97657 centroids, pick 131072 (next power of 2),
#     min-train = 5,111,808, avg-train = 16,777,216, max-train = 33,554,432
#     min-RAM = 19.9GB, max-RAM = 131GB, so we need 2 10GB batches at min-data or
#     9 14.5GB batches to train at max-data with the available RAM
# - additional vector index specifications facets:
#   - ram=16GB, nlist=None (use 8K size to compute if not provided), nlist=8, niter=25


class NearestNeighborIndex(object):
    """Index object that speeds up nearest-neighbor search operations over the vectors
    in a vector store.
    """

    def __init__(self, store):
        """Initialize a nearest neighbor index for the vector store 'store'.
        """
        self.vector_store = store
        self.sql_store = self.vector_store.store

    def is_trained(self):
        """Return True if this index has a trained quantizer.
        """
        raise KGTKException('not implemented')

    def create(self, force=False, explain=False):
        """Top-level entry point that builds the index for the current set of vectors in the vector store,
        unless it has already been built previously, or if 'force' is True.  Depending on the respective
        index spec parameters, this may take a long time to compute.  If 'explain' is True, only describe
        the steps that would be taken, but do not actually build the index.
        """
        raise KGTKException('not implemented')
    
    def drop(self, explain=False):
        """Top-level entry point that deletes the index for the current set of vectors in the vector store.
        If 'explain' is True, only describe the steps that would be taken, but do not actually drop the index.
        """
        # no-op by default:
        pass
    
    def search(self, vectors, k=1, nprobe=None):
        """Search this index for the 'k' nearest neighbors of 'vectors' and return
        the result as a tuple D, V (where D are distances and V vector IDs).
        'nprobe' controls how deep the index will be searched.
        """
        raise KGTKException('not implemented')

    
class FaissIndex(NearestNeighborIndex):
    """Nearest-neighbor index implemented via calls to the FAISS library.
    The current implementation basically creates a database-centered
    faiss.IndexIVFFlat index that creates a small quantizer which gets
    loaded into memory and then very efficiently loads previously quantized
    vectors from the DB during search.  This basically creates a disk-based
    FAISS index which allows us to create, train and search very large indexes
    without having to load all vectors into RAM.  While FAISS has some limited
    and somewhat crufty on-disk support, it still requires large amounts of
    RAM to train such indexes, and the vectors are stored as part of the
    index which makes our Kypher interactions with them more difficult.
    """

    FAISS_FLOAT_TYPE = np.float32    # uniform float type used by FAISS C++ API
    FAISS_VECTOR_ID_TYPE = np.int64  # type for numeric vector IDs
    DEFAULT_CENTROID_SIZE = 8192
    DEFAULT_MIN_POINTS_PER_CENTROID = 39
    DEFAULT_MAX_POINTS_PER_CENTROID = 256
    DEFAULT_MAX_ALLOWED_RAM = 16 * 1024 * 1024 * 1024
    DEFAULT_NITER = 10
    DEFAULT_NPROBE = 8
    MIN_TEMP_TABLE_SIZE = 2 ** 31    # 2GB, assume temp tables can be at least this big
    
    # if true, incrementally grow the search index for more and more qcells up to a limit;
    # this is primarily here to allow us to turn this off for debugging or memory issues:
    REUSE_SEARCH_INDEX = True
    
    def __init__(self, store):
        """Initialize a FAISS nearest neighbor index for the vector store 'store'.
        """
        super().__init__(store)
        self.index_options = None
        self.vector_ndim = None
        self.vector_dtype = None
        self.vector_norm = None
        self.ntotal = None
        self.nlist = None
        self.nbatches = None
        self.batch_size = None
        self.niter = None
        self.nprobe = None
        self.data_buffer = None
        self.clustering = None
        self.quantizer = None
        self.search_index = None
        self.search_index_qcells = None
        self.search_index_max_size = None
        self.compute_parameters()

    def compute_parameters(self):
        """Initialize any undefined parameters based on the linked vector store.
        """
        vstore = self.vector_store
        if self.index_options is None:
            self.index_options = vstore.get_vector_index_options()
        if self.vector_ndim is None:
            self.vector_ndim = vstore.get_vector_ndim()
        if self.vector_dtype is None:
            self.vector_dtype = vstore.get_vector_dtype()
        if self.vector_norm is None:
            self.vector_norm = vstore.get_vector_norm()
        if self.ntotal is None:
            self.ntotal = vstore.get_store_ntotal()
        if self.nlist is None:
            self.nlist = self.index_options.get('nlist')
            if self.nlist is None:
                # pick closest power of 2 based on default centroid size:
                self.nlist = 1 << round(math.log2(self.ntotal / self.DEFAULT_CENTROID_SIZE))
        if self.niter is None:
            self.niter = self.index_options.get('niter') or self.DEFAULT_NITER
        if self.nprobe is None:
            self.nprobe = self.index_options.get('nprobe') or self.DEFAULT_NPROBE
        if self.batch_size is None:
            nbytes = np.zeros(1, dtype=self.FAISS_FLOAT_TYPE).nbytes
            min_ram = self.vector_ndim * nbytes * self.nlist * self.DEFAULT_MIN_POINTS_PER_CENTROID
            max_ram = self.vector_ndim * nbytes * self.nlist * self.DEFAULT_MAX_POINTS_PER_CENTROID
            max_allowed_ram = self.index_options.get('ram') or self.DEFAULT_MAX_ALLOWED_RAM
            max_allowed_ram *= 0.8 # safety cushion for other buffers, etc.
            if max_ram <= max_allowed_ram:
                # single batch, pick max data size that doesn't trigger FAISS subsampling:
                self.batch_size = min(self.nlist * self.DEFAULT_MAX_POINTS_PER_CENTROID, self.ntotal)
                self.nbatches = 1
            elif min_ram <= max_allowed_ram:
                # single batch, pick as many vectors as we can fit into available RAM:
                self.batch_size = max_allowed_ram / ( self.vector_ndim * nbytes )
                self.nbatches = 1
            else:
                # multi-batch training required which likely means that we have a lot of data,
                # so train based on the minimum number of data points recommended by FAISS:
                self.nbatches = math.ceil(min_ram / max_allowed_ram)
                self.batch_size = self.nlist * self.DEFAULT_MIN_POINTS_PER_CENTROID // self.nbatches
       
    def ensure_float_type(self, array):
        """Coerce 'array' to float32 if necessary, which is the float type the FAISS API expects.
        """
        if array.dtype != self.FAISS_FLOAT_TYPE:
            return array.astype(self.FAISS_FLOAT_TYPE)
        else:
            return array

    def ensure_vector_id_type(self, array):
        """Coerce 'array' to int64 if necessary, which is the vector ID type the FAISS API expects.
        """
        if array.dtype != self.FAISS_VECTOR_ID_TYPE:
            return array.astype(self.FAISS_VECTOR_ID_TYPE)
        else:
            return array

    def ensure_vector_array(self, array):
        """Make sure 'array' is a 2-d array of vectors (in case only a single vector was provided).
        """
        if len(array.shape) == 2:
            return array
        elif len(array.shape) == 1:
            return array.reshape((1, array.shape[0]))
        else:
            raise KGTKException('cannot reshape array into 2-d form')
        
    def get_data_buffer(self):
        """Allocate a data buffer that can be used to hold self.batch_size vectors.
        """
        if self.data_buffer is None:
            self.data_buffer = np.zeros(self.batch_size * self.vector_ndim, dtype=self.FAISS_FLOAT_TYPE)
            self.data_buffer.shape = (self.batch_size, self.vector_ndim)
        return self.data_buffer

    def get_quantizer_file(self, shardid=''):
        """Return a file name that can be used to store the trained quantizer index.
        """
        # TO DO: consider storing the quantizer as a BLOB object in the database
        vstore = self.vector_store
        vsname = vstore.get_store_name()
        if shardid and not shardid.endswith('.'):
            shardid += '.'
        return f'{vstore.get_sqlstore_dbfile()}.vec.{vsname}.faiss.{shardid}idx'

    def get_quantizer(self, error=True):
        """Return the quantizer for this vector store, raise an error if it doesn't exist
        unless 'error' is False.
        """
        if self.quantizer is None:
            qfile = self.get_quantizer_file()
            if os.path.exists(qfile):
                self.quantizer = faiss.read_index(qfile)
            elif error:
                raise KGTKException(f"cannot find quantizer for this vector store: {qfile}")
        return self.quantizer

    def is_trained(self):
        """Return True if this index has a trained quantizer.
        """
        return self.get_quantizer(error=False) is not None and self.quantizer.is_trained

    def train_quantizer_single_batch(self):
        # this could be run as a special case of multi-batch, but just in case it is
        # more advantageous to do all iterations at once, we implement this separately:
        clus = faiss.Clustering(self.vector_ndim, self.nlist)
        clus.niter = self.niter
        clus.verbose = self.sql_store.loglevel > 0
        if self.vector_norm == ispec.VectorIndex.NORM_L2:
            clus.index = faiss.IndexFlatIP(self.vector_ndim)
        else:
            clus.index = faiss.IndexFlatL2(self.vector_ndim)
        self.clustering = clus
        self.quantizer = clus.index
        vstore = self.vector_store
        buffer = self.get_data_buffer()
        # TO DO: support random sampling of batches
        buffer, nvec = vstore.get_vectors_as_array(self.batch_size, offset=0, buffer=buffer)
        self.sql_store.log(1, f'Training vector store quantizer:')
        clus.train(buffer[0:nvec], clus.index)
        self.sql_store.log(1, '\n') # kludge: ensure newline after clustering log output
        return clus

    def train_quantizer_multi_batch(self):
        clus = faiss.Clustering(self.vector_ndim, self.nlist)
        clus.niter = 1
        clus.verbose = self.sql_store.loglevel > 0
        if self.vector_norm == ispec.VectorIndex.NORM_L2:
            clus.index = faiss.IndexFlatIP(self.vector_ndim)
        else:
            clus.index = faiss.IndexFlatL2(self.vector_ndim)
        self.clustering = clus
        self.quantizer = clus.index
        vstore = self.vector_store
        buffer = self.get_data_buffer()
        # TO DO: figure out whether we should use the 'nredo' parameter for this instead:
        for i in range(self.niter):
            cursor = 0
            self.sql_store.log(1, f'Training vector store quantizer iteration {i+1}:')
            for b in range(self.nbatches):
                # TO DO: support random sampling of batches, for the multi-batch case we also
                #        need to ensure that we get the same sampled batches in each iteration
                buffer, nvec = vstore.get_vectors_as_array(self.batch_size, offset=cursor, buffer=buffer)
                clus.train(buffer[0:nvec], clus.index)
                cursor += nvec
        return clus

    def train_quantizer(self, explain=False):
        """Train and save a quantizer index for this vector store.
        If 'explain' just explain what is going to be done without doing it.
        """
        if explain:
            # for now, elaborate description of process:
            self.sql_store.log(0, 'Training quantizer...')
            return
        if self.nbatches == 1:
            self.train_quantizer_single_batch()
        else:
            self.train_quantizer_multi_batch()
        faiss.write_index(self.quantizer, self.get_quantizer_file())

    def quantize_vectors(self, explain=False):
        """Quantize the vectors in this vector store with the previously trained quantizer.
        This will quantize each vector in the database and associate it with its qcell in
        its corresponding graph table.  If 'explain' just explain what is going to be done
        without doing it.
        """
        quantizer = self.get_quantizer()
        temp_table = f'_qcell_temp_{abs(hash(self.quantizer))}'
        temp_schema = sdict['_name_': temp_table, 'columns': sdict['qcell': sdict['_name_': 'qcell', 'type': 'TEXT']], 'temporary': True]
        sstore = self.sql_store
        vstore = self.vector_store
        vstable = vstore.table
        sstore.execute(sstore.get_table_definition(temp_schema))
        # TO DO: ensure that we always have a large enough batch size for this:
        buffer = self.get_data_buffer()
        cursor = 0
        sstore.log(1, f'Quantizing {self.ntotal} vectors in batches of size {self.batch_size}...')
        while cursor < self.ntotal:
            vecs, nvec = vstore.get_vectors_as_array(self.batch_size, offset=cursor, buffer=buffer)
            cursor += nvec
            D, V = quantizer.search(vecs[0:nvec], 1)
            sstore.executemany(f'INSERT INTO {temp_table} VALUES (?)', map(lambda x: (str(x[0]),), V))
            if sstore.loglevel > 0:
                sys.stderr.write('.')
                sys.stderr.flush()
        if sstore.loglevel > 0:
            sys.stderr.write('\n')
        sstore.log(1, f'Adding quantization index to database...')
        qcell_colname = vstore.get_quantizer_cell_column_name()
        qcell_index_spec = ispec.TableIndex(vstable, qcell_colname)
        header = sstore.get_table_header(vstable)
        if qcell_colname not in header:
            sstore.execute(f'ALTER TABLE {vstable} ADD COLUMN {sql_quote_ident(qcell_colname)} TEXT')
        elif sstore.has_graph_index(vstable, qcell_index_spec):
            # we have an index from a prior quantization, delete it since we need to rebuild it from scratch:
            sstore.drop_graph_index(vstable, qcell_index_spec)
        sstore.execute(
            f"""UPDATE {vstable}
                SET {sql_quote_ident(qcell_colname)} = {temp_table}.qcell
                FROM {temp_table}
                WHERE {vstable}.rowid = {temp_table}.rowid""")
        self.sort_vectors()
        sstore.ensure_graph_index(vstable, qcell_index_spec, commit=False)

    def sort_vectors(self):
        """Sort the vectors in the associated vector store by q-cell ID for improved locality during search.
        """
        # TO DO: this should become a method on vector stores
        sstore = self.sql_store
        vstore = self.vector_store
        if isinstance(vstore, InlineVectorStore):
            qcell_colname = vstore.get_quantizer_cell_column_name()
            # KLUDGE: sorting the vector table can be extremely space intensive without batching and committing
            # batches (up to 3-4x the space requirements for the table itself), so we re-enter auto-commit mode
            # here so that sort_table can manage its own transactions - this means there is a chance that the
            # DB winds up in a "slightly" inconsistent stage if something breaks during sorting:
            sstore.commit()
            # estimate final table size here, since it won't be measured and recorded until later:
            nbytes = np.zeros(1, dtype=self.vector_dtype).nbytes
            table_size = int(nbytes * self.vector_ndim * self.ntotal * 1.2)
            # use fewer batches for smaller tables, but stay between 2 and 10:
            nbatches = min(max(math.ceil(table_size / self.MIN_TEMP_TABLE_SIZE), 2), 10)
            sstore.batched_sort_table(vstore.table, f'CAST({sql_quote_ident(qcell_colname)} AS INT)', n=nbatches, commit=True)
        else:
            sstore.log(0, 'WARNING: sorting on this type of vector store not yet implemented')

    def create(self, force=False, explain=False):
        """Top-level entry point that builds the index for the current set of vectors in the vector store,
        unless it has already been built previously, or if 'force' is True.  Depending on the respective
        index spec parameters, this may take a long time to compute.  If 'explain' is True, only describe
        the steps that would be taken, but do not actually build the index.
        """
        if not self.is_trained() or force:
            self.train_quantizer(explain=explain)
            self.quantize_vectors(explain=explain)

    def drop(self, explain=False):
        """Top-level entry point that deletes the index for the current set of vectors in the vector store.
        If 'explain' is True, only describe the steps that would be taken, but do not actually drop the index.
        """
        loglevel = 0 if explain else 1
        if self.is_trained():
            qfile = self.get_quantizer_file()
            self.sql_store.log(loglevel, f"DELETING NN-index quantizer file '{qfile}'")
            if not explain:
                # we only remove the quantizer file for now, we do not also remove the qcell
                # column, since it is harmless and will most likely be replaced with a new one:
                os.remove(qfile)
                # reinitialize to remove any stale cached information:
                self.__init__(self.vector_store)

    def get_search_index(self, reuse=False):
        """Return a FAISS index that can be used to search a query vector against all vectors from relevant q-cells.
        This index is created dynamically during a query, linked to a pre-trained quantizer and then quickly populated
        with relevant vectors retrieved from the database using the 'index.add_core' method.  It uses a fast,
        multi-threaded, heap-based search implementation by FAISS which beats anything we might create from scratch.
        """
        # if the index exists and 'reuse' is True, we reuse the index in a size-limited fashion, that is only
        # if the total size occupied by the currently indexed vectors is less than the max RAM for the index;
        # reuse speeds things up significantly (5x or more) and basically incrementally loads a full FAISS index
        # up to the specified RAM limit:
        if self.search_index is None or not reuse or self.search_index.ntotal > self.search_index_max_size:
            quantizer = self.get_quantizer()
            self.search_index = faiss.IndexIVFFlat(quantizer, self.vector_ndim, self.nlist, quantizer.metric_type)
            self.search_index.is_trained = True
            self.search_index.verbose = self.sql_store.loglevel >= 2
            self.search_index_qcells = set()
            # compute a maximum number of vectors to store in the index:
            # TO DO: factor out these memory computations into some utility functions
            max_allowed_ram = self.index_options.get('ram') or self.DEFAULT_MAX_ALLOWED_RAM
            max_allowed_ram *= 0.8 # safety cushion for other buffers, etc.
            nbytes = np.zeros(1, dtype=self.FAISS_FLOAT_TYPE).nbytes
            self.search_index_max_size = int(max_allowed_ram // (self.vector_ndim * nbytes))
        # just doing this doesn't free up memory for some reason, so we eventually run out of RAM:
        #elif not reuse:
        #    self.search_index.reset()
        #    self.search_index.nprobe = 1
        return self.search_index

    def get_search_index_for_qcells(self, qcells):
        """Return a search index that contains (at least) all vectors of the identified 'qcells'.
        """
        # NOTE: having more qcells stored in the index than asked for in 'qcells' does not affect the results,
        # since those are the nprobe nearest neighbors from running a vector V through the quantizer, which will
        # be the same qcells selected when V is searched against the full index with the given nprobe;
        # TO DO: figure out what the speedup is from running multiple vectors through the search instead of 1-by-1
        index = self.get_search_index(reuse=self.REUSE_SEARCH_INDEX)
        loaded_qcells = self.search_index_qcells
        vstore = self.vector_store
        for row in self.ensure_vector_array(qcells):
            for qcell in row:
                # -1 is a FAISS code for "not found":
                if qcell >= 0 and qcell not in loaded_qcells:
                    vecs, vecids = vstore.get_qcell_vectors(qcell)
                    nvecs = len(vecs)
                    vecs = self.ensure_float_type(vecs)
                    vecids = self.ensure_vector_id_type(vecids)
                    qcellids = np.zeros(nvecs, dtype=self.FAISS_VECTOR_ID_TYPE)
                    qcellids[:] = qcell
                    # we use 'add_core' which is very fast, since we already know the qcell IDs of the added vectors:
                    index.add_core(nvecs, faiss.swig_ptr(vecs), faiss.swig_ptr(vecids), faiss.swig_ptr(qcellids))
                    loaded_qcells.add(qcell)
        return index
    
    def search_quantizer(self, vectors, k=None):
        """Search the top-'k' qcells for each of 'vectors' in the current quantizer.
        'k' here corresponds to the 'nprobe' parameter used in the FAISS API, that is,
        it controls how many close qcells are exhaustively searched for each query vector.
        """
        k = min(k or self.nprobe, self.nlist)
        vectors = self.ensure_float_type(vectors)
        vectors = self.ensure_vector_array(vectors)
        D, V = self.get_quantizer().search(vectors, k)
        return D, V

    def get_search_index_for_vectors(self, vectors, nprobe=None):
        """Create a reusable search index for 'vectors' (for dynamic scaling).
        'nprobe' controls how many inverted lists will be searched (defaults to self.nprobe)
        """
        vectors = self.ensure_float_type(vectors)
        vectors = self.ensure_vector_array(vectors)
        _, qcells = self.search_quantizer(vectors, k=nprobe)
        index = self.get_search_index_for_qcells(qcells)
        # IMPORTANT: by default the nprobe value of the IndexIVFFlat index is set to 1, and there is no parameter
        # that allows us to control that from the 'search' method, so we set it here to correspond to 'nprobe':
        index.nprobe = max(nprobe or self.nprobe, 1)
        return index
    
    def search(self, vectors, k=1, nprobe=None, index=None):
        """Search this index for the 'k' nearest neighbors of 'vectors' and return
        the result as a tuple D, V (where D are distances and V vector IDs).  'nprobe'
        controls how many inverted lists will be searched (defaults to self.nprobe).
        """
        vectors = self.ensure_float_type(vectors)
        vectors = self.ensure_vector_array(vectors)
        if index is None:
            index = self.get_search_index_for_vectors(vectors, nprobe=nprobe)
        k = min(k, index.ntotal)
        D, V = index.search(vectors, k)
        return D, V
