"""
VectorStore to support Kypher queries over embedding and other vectors.
"""

import sys
import os
import os.path
import numpy as np
import h5py

from   kgtk.exceptions import KGTKException


### VectorStore

class VectorStore(object):
    """Auxiliary vector store to store and access embeddings and other vectors.
    """

    MAX_OPEN_DATASETS = 256
    
    def __init__(self, store):
        """Create and/or open an auxiliary VectorStore for the SQL store 'store'.
        """
        self.store = store
        # a vector cache is tightly linked to its parent SQL store, so we use a fixed pattern here:
        self.dbfile = store.dbfile + '.vec.hdf5'
        self.conn = None
        self.dataset_ids = {}
        self.datasets = [None] * self.MAX_OPEN_DATASETS

    def get_conn(self, mode='r'):
        """Return the HD5 file connection object for this store, open it if necessary
        according to 'mode'.  If it is already open in read mode but a write-mode is
        requested, close it and reopen it according to the new mode (unless the underlying
        SQL store is in read-only mode).  We only upgrade the mode from 'r' to 'r+' if
        needed, we never go the other direction.
        """
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
            self.conn.close()
            self.conn = h5py.File(self.dbfile, mode)
        return self.conn

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def commit(self):
        self.close()

    def get_dataset_name(self, table, column):
        return f'{table}:{column}'

    def get_dataset_id(self, table, column):
        """Return a numneric dataset ID for 'table->column' that can later be used
        to access dataset objects for this dataset efficiently during queries.
        """
        key = (table, column)
        dsid = self.dataset_ids.get(key)
        if dsid is None:
            dsid = len(self.dataset_ids)
            self.dataset_ids[key] = dsid
        if dsid >= self.MAX_OPEN_DATASETS:
            raise KGTKException(f"too many open vector datasets, max is {self.MAX_OPEN_DATASETS}")
        return dsid

    def get_vector_dataset(self, table, column):
        """Return a vector dataset object for 'table->column' if it exists, None otherwise.
        """
        return self.get_conn().get(self.get_dataset_name(table, column))

    def get_vector_dataset_by_id(self, dsid):
        """Return a vector dataset object for the dataset registered under 'dsid'.
        Raise an error if no such dataset ID exists.
        """
        for (table, column), regid in self.dataset_ids.items():
            if regid == dsid:
                return self.get_vector_dataset(table, column)
        else:
            raise KGTKException(f"no registered dataset with ID {dsid}")

    def drop_vector_dataset(self, table, column):
        """If a vector dataset object for 'table->column' exists, delete it, no-op otherwise.
        """
        ds = self.get_vector_dataset(table, column)
        if ds is not None:
            del self.get_conn(mode='r+')[self.get_dataset_name(table, column)]

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

    def parse_vectors(self, vectors, fmt='auto', dtype=np.float32):
        if fmt != 'auto':
            raise KGTKException(f"cannot handle vector format '{fmt}'")
        vectors = list(vectors)
        if len(vectors) == 0:
            return vectors
        fmt, sep = self.guess_vector_format(vectors[0])
        # parsing text vectors into arrays takes the most time of an import (about the same
        # as uncompressing the data with the gzip library); we tried various other things
        # np.loadtxt, parsing into list to array, json.loads, etc., but to no significant
        # improvement, so we stick with this for now:
        return [np.fromstring(vec, dtype=dtype, sep=sep) for vec in vectors]

    def import_vectors(self, table, column, source_vectors, fmt='auto', dtype=np.float32):
        """Parse a collection of 'source_vectors' according to 'fmt' and 'dtype' into a
        two-dimensional numpy array of vectors, and incrementally add them to end of the
        vector dataset for 'table->column' (which will be created if necessary).
        """
        vectors = self.parse_vectors(source_vectors, fmt=fmt, dtype=dtype)
        if len(vectors) == 0:
            return
        ds = self.get_vector_dataset(table, column)
        if ds is None:
            dsname = self.get_dataset_name(table, column)
            ndim = len(vectors[0])
            chunksize = self.store.VECTOR_IMPORT_CHUNKSIZE
            conn = self.get_conn(mode='r+')
            # we need chunking so we can resize, otherwise we'd have to know the number of vectors ahead of time;
            # we use auto-chunking for now, but maybe supplying an explicit shape would be better - maybe later:
            ds = conn.create_dataset(dsname, dtype=dtype, shape=(0,ndim), maxshape=(None,ndim), chunks=True)
        size, ndim = ds.shape
        ds.resize(size + len(vectors), axis=0)
        ds[size:] = vectors

    def get_vector(self, vecspec):
        """Return the numpy vector for 'vecspec' as generated by 'sqlstore._kgtk_get_vector_spec'.
        """
        if isinstance(vecspec, int):
            dsid = vecspec & 0xf
            rowid = vecspec >> 8
        else:
            # TO DO: consider dynamic parsing of string vector representations, so we can run vector
            # operations on embeddings even if they haven't been specially imported or indexed:
            raise KGTKException(f"unhandled vector spec format'")
        ds = self.datasets[dsid]
        if ds is None:
            ds = self.get_vector_dataset_by_id(dsid)
            self.datasets[dsid] = ds
        # TO DO: consider reading into pre-allocated vector buffers instead of creating dynamic array copies:
        # this is what is most expensive right now, takes about 0.1ms / call which is probably not all that
        # different from just parsing the source....20,000 calls take about 2secs
        return ds[rowid]
