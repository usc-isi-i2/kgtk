"""
'VectorFunction's to support Kypher queries and computations over vectors.
"""

import numpy as np

from   kgtk.exceptions import KGTKException
from   kgtk.kypher.utils import *
import kgtk.kypher.indexspec as ispec
from   kgtk.kypher.functions import SqlFunction, VirtualGraphFunction
from   kgtk.kypher.vecstore import MasterVectorStore, InlineVectorStore
import kgtk.kypher.parser as parser


### NOTES

# To properly access and efficiently compute with indexed vector data we have to support
# two basic operations:
#
# (1) graph variable access: when a graph variable corresponding to a vector column is
# referenced in a Kypher query (e.g., in a 'where' or 'return'-clause), it has to
# generate an appropriate vector object.  For columns indexed via an 'inline'-store this
# is automatic, the value will simply be the byte string representing the BLOB value of
# the encoded vector column.  For external array-based stores ('numpy' and 'hd5') we have
# to substitute the variable reference with a function call that brings in the vector
# object from the secondary store.  This is done by creating calls to '_kvec_get_vector'
# which takes the 'rowid' of the graph column as its argument and retrieves the bytes
# from the corresponding store based on that index (during import each vector at 'rowid=N'
# will be stored at position 'store[N-1]' in the external store, since row IDs are 1-based).
# The Kypher query translator calls 'SqlStore.vector_column_to_sql' to generate these
# accesses, which in turn will call out to the appropriate graph table.column vector store.
# The 'KvecGetVector' function below will create a call-specific function object that
# has an efficient cache for the required vector store handle built-in.
#
# (2) function calls processing or returning vectors: functions called by the SQLite query
# engine can only be passed and return literal data types and binary BLOB values (represented
# as byte strings in the Python API).  This means we cannot pass Python objects such as NumPy
# vectors from one function to another (e.g., the result of a '_kvec_get_vector' call).
# This means we have to either convert a NumPy vector to its underlying bytes before passing
# or returning, or we create special-purpose optimized translations for certain situations
# (in the current implementation we use both schemes).  For example, a call of a vector
# function in a Kypher query such as, for example,
#    kvec_dot_product(v1, v2)
# can be translated into this if both variables correspond to (compatible) inline stores:
#    kvec_dot_product_inline(graph_1_c1.node2, graph_1_c2.node2)
# Alternatively, if the variables correspond to a NumPy store, this translation can be used:
#    kvec_dot_product_array(graph_1_c1.rowid, graph_1_c2.rowid)
# A generic call can first create bytes and then pass them to the underlying function like so:
#    kvec_dot_product_generic(_kvec_get_vector(graph_1_c1.rowid), _kvec_get_vector(graph_1_c2.rowid))
# The function object 'DotProduct' handles the context-specific translations and will try to
# use optimized calls where possible or a generic call if optimization can't be done.  It will
# also create call-specific custom function pointers (closures) that encapsulate all the
# necessary state and cache information (e.g., store handles, vector dtypes, etc.) so that
# they do not need to be passed in or determined at run time for optimal efficiency.
#
# The function objects below can do further query-translation-time optimizations.  For example,
# 'CosineSimilarity' can check whether the corresponding vector columns were appropriately
# normalized, and, if so, can subsitute a cheaper dot-product computation.


class VectorFunction(SqlFunction):
    """General function class supporting vector computations.
    """
    DEFAULT_DTYPE = np.dtype(np.float32)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uniquify = True
        self.xstore = None     # used to hold the vector store corresponding to the first x argument
        self.ystore = None     # used to hold the vector store corresponding to the second y argument
        self.optimize = False  # internal switch to flag whether to produce optimized or generic code

    def get_argument_vector_store(self, query, arg, state, clause=None):
        """If 'arg' is a column variable that can be linked to a vector store,
        return the associated vector store object, otherwise return None.
        If 'clause' is not None, it should be the pattern clause containing 'arg',
        in which case the graph associated with that clause will dominate 'arg's.
        As the second return value, return the optimized reference that can
        be used for the vector for this type of vector store.
        """
        # TO DO: figure out whether we need to worry about join-variables here
        # that can't be linked unambiguously to a table, but then joins on 
        # vector columns don't really make sense, do they (unless vectors
        # become inputs to other vector computations)?
        if isinstance(arg, parser.Variable):
            graph, column, sql = query.variable_to_sql(arg, state)
            table = state.get_alias_table(graph)
            if clause is not None:
                # make the clause graph dominate, so we can join across vector tables:
                table = query.get_pattern_clause_graph(clause)
                # pick an arbitrary alias for this table, they'll be joined if there is more than one,
                # but maybe we should pick the one specific to this clause - but there is no mechanism yet:
                #graph = state.get_table_aliases(table)[0]
            master = self.store.get_vector_store()
            # TO DO: maybe add an 'error' arg to 'get_vector_store' so we can simplify this test:
            if master.has_vector_store(table, column) or self.store.is_vector_column(table, column):
                vstore = master.get_vector_store(table, column)
                vref = vstore.vector_column_to_reference_sql(table_alias=graph)
                return vstore, vref
        return None, None

    def get_call_context(self):
        """Define a set of closure variables needed to define optimized vector operation code.
        If uniquify=True (the default), these will be specific to a single call location in a 
        query and not be shared across calls or queries.  NOTE: the default dtypes here are
        intended for the generic call case where we might not know, for example, in case an
        argument is provided through another function call.
        """
        sql_store, xstore, ystore = self.store, self.xstore, self.ystore
        # for now, if we have a vector argument that does not come from a vector store and,
        # hence, we don't know its dtype, we assume and coerce everything to DEFAULT_DTYPE:
        xtable, xcolumn, xdtype = None, None, self.DEFAULT_DTYPE
        xcache = [None, None]
        if xstore is not None:
            xtable = xstore.table
            xcolumn = xstore.column
            xdtype = xstore.get_vector_dtype()
        ytable, ycolumn, ydtype = None, None, self.DEFAULT_DTYPE
        ycache = [None, None]
        if ystore is not None:
            ytable = ystore.table
            ycolumn = ystore.column
            ydtype = ystore.get_vector_dtype()
        return sql_store, xtable, xcolumn, xdtype, xcache, ytable, ycolumn, ydtype, ycache

    def translate_one_arg_call_to_optimized_sql(self, query, expr, state):
        args = expr.args
        if len(args) != 1:
            raise KGTKException(f"Illegal number of arguments to '{self.get_name()}'")
        self.xstore, xref = self.get_argument_vector_store(query, args[0], state)
        self.optimize = self.xstore
        if self.optimize:
            # we produce an optimized call operating on vector references:
            arg = xref
        else:
            # otherwise, arg is assumed to yield a byte-string encoding a vector:
            arg = query.expression_to_sql(args[0], state)
        self.load()
        return f'{self.get_name()}({arg})'

    def translate_one_arg_call_to_generic_sql(self, query, expr, state):
        args = expr.args
        if len(args) != 1:
            raise KGTKException(f"Illegal number of arguments to '{self.get_name()}'")
        self.xstore, xref = self.get_argument_vector_store(query, args[0], state)
        self.optimize = False
        # arg is assumed to yield a byte-string encoding a vector:
        arg = query.expression_to_sql(args[0], state)
        self.load()
        return f'{self.get_name()}({arg})'
    
    def translate_two_arg_call_to_optimized_sql(self, query, expr, state):
        args = expr.args
        if len(args) != 2:
            raise KGTKException(f"Illegal number of arguments to '{self.get_name()}'")
        self.xstore, xref = self.get_argument_vector_store(query, args[0], state)
        self.ystore, yref = self.get_argument_vector_store(query, args[1], state)
        self.optimize = self.xstore and self.ystore and type(self.xstore) == type(self.ystore)
        if self.optimize:
            # we produce an optimized call operating on vector references:
            args = [xref, yref]
        else:
            # otherwise, each arg is assumed to yield a byte-string encoding a vector:
            args = [query.expression_to_sql(arg, state) for arg in args]
        self.load()
        return f'{self.get_name()}({", ".join(args)})'
    
    def translate_two_arg_call_to_generic_sql(self, query, expr, state):
        args = expr.args
        if len(args) != 2:
            raise KGTKException(f"Illegal number of arguments to '{self.get_name()}'")
        self.xstore, xref = self.get_argument_vector_store(query, args[0], state)
        self.ystore, yref = self.get_argument_vector_store(query, args[1], state)
        self.optimize = False
        # each arg is assumed to yield a byte-string encoding a vector:
        args = [query.expression_to_sql(arg, state) for arg in args]
        self.load()
        return f'{self.get_name()}({", ".join(args)})'


class GenericVectorFunction(VectorFunction):
    """Function class for simple vector functions that only implement a generic computation.
    """

    def translate_call_to_sql(self, query, expr, state):
        if self.num_params == 1:
            return self.translate_one_arg_call_to_generic_sql(query, expr, state)
        elif self.num_params == 2:
            return self.translate_two_arg_call_to_generic_sql(query, expr, state)
        else:
            raise KGTKException(f"don't know how to translate '{self.get_name()}' with {self.num_params} parameters")

    def get_generic_code(self):
        """Generic calls assume byte strings as inputs which either come directly from the DB
        or via '_kvec_get_vector' calls or as results from vector computations.
        """
        raise KGTKException('not implemented')
        
    def get_code(self):
        if self.code is None:
            self.code = self.get_generic_code()
            self.name += '_generic'
        return self.code


class KvecGetVector(VectorFunction):
    """Access the vector corresponding to a vector-indexed column variable as a string of bytes.
    This is an internal accessor needed to retrieve vectors from Numpy and HD5 vector stores.
    """

    def get_code(self):
        if self.code is None:
            if self.xstore is None:
                raise KGTKException(f"missing vector store for call to '{self.get_name()}'")
            elif isinstance(self.xstore, InlineVectorStore):
                def _kvec_get_vector(vector):
                    return vector
            else:
                sstore, xtab, xcol, xdtype, xcache, _, _, _, _ = self.get_call_context()
                def _kvec_get_vector(rowid):
                    vs = xcache[0]
                    if vs is None:
                        # this will initialize the cache to the proper store handle upon the first call:
                        vs = MasterVectorStore.get_vector_store_as_array(sstore, xtab, xcol, cache=xcache)
                    return vs[rowid - 1].tobytes()
            self.code = _kvec_get_vector
        return self.code

    def load(self):
        if isinstance(self.xstore, InlineVectorStore):
            # not needed for inline stores:
            return
        super().load()

KvecGetVector('_kvec_get_vector', num_params=1, deterministic=True).define()


class DotProduct(VectorFunction):
    """Compute the dot product between two vectors x and y.
    """

    # The implementation below is somewhat complex and shows the different kinds of optimizations
    # that are possible.  However, the generic call scheme is identical with the optimized scheme
    # for inline-store vectors, and will be just slightly slower for array-store vectors compared
    # to their optimized versions.  So a streamlined version could eliminate all optimizations and
    # simply implement the generic call scheme only, with just a very minor performance penalty.
    # However, we keep this for now as documentation for what can be done.
    
    def translate_call_to_sql(self, query, expr, state):
        return self.translate_two_arg_call_to_optimized_sql(query, expr, state)
        # for measuring improvements coming from optimized translations:
        #return self.translate_two_arg_call_to_generic_sql(query, expr, state)

    def get_optimized_code_inline(self):
        """Return optimized code operating on two arguments corresponding to inline vector stores.
        Since those will be byte strings coming directly from the corresponding graph table columns,
        no specific vector access is required and both 'x' and 'y' will be bound to bytes.
        """
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        def _dot_product(x, y):
            # 'frombuffer' calls are very fast, O(1):
            vx = np.frombuffer(x, dtype=xdtype)
            vy = np.frombuffer(y, dtype=ydtype)
            # make sure we don't return numpy floats:
            return float(np.dot(vx, vy))
        return _dot_product

    def get_optimized_code_array_v1(self):
        """Return optimized code operating on two arguments corresponding to vector stores that
        can be accessed via array handles (numpy and hd5).  Arguments will be rowid's which are
        used to access the corresponding vectors from the array handles.
        """
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        def _dot_product(xrowid, yrowid):
            # this is about 2x slower for the numpy store compared to inline, hd5 is much much slower than
            # that due to the individual array accesses causing significant per-call overhead; we tried
            # various tweaks on this for numpy, but this is about as fast as we can make it for now:
            xvs = xcache[0]
            if xvs is None:
                # this will initialize caches to the proper store handles upon the first call:
                xvs = MasterVectorStore.get_vector_store_as_array(sstore, xtab, xcol, cache=xcache)
                yvs = MasterVectorStore.get_vector_store_as_array(sstore, ytab, ycol, cache=ycache)
            # make sure we don't return numpy floats:
            return float(np.dot(xvs[xrowid - 1], ycache[0][yrowid - 1]))
        return _dot_product

    def get_optimized_code_array_v2(self):
        """Variant of 'get_optimized_code_array_v1' that copies vectors into local cache vector buffers
        to avoid any np array allocations.  This is very slightly faster than v1 but probably doesn't
        warrant the extra complexity.
        """
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        def _dot_product(xrowid, yrowid):
            xv = xcache[1]
            yv = ycache[1]
            if xv is None:
                # this will initialize caches to the proper store handles upon the first call:
                MasterVectorStore.get_vector_store_as_array(sstore, xtab, xcol, cache=xcache)
                MasterVectorStore.get_vector_store_as_array(sstore, ytab, ycol, cache=ycache)
                xv = np.zeros(len(xcache[0][xrowid - 1]), dtype=xdtype)
                yv = np.zeros(len(ycache[0][yrowid - 1]), dtype=ydtype)
                xcache[1], ycache[1] = xv, yv
            xv[:] = xcache[0][xrowid - 1]
            yv[:] = ycache[0][yrowid - 1]
            # make sure we don't return numpy floats:
            return float(np.dot(xv, yv))
        return _dot_product

    def get_generic_code(self):
        """Generic calls assume byte strings as inputs which either come directly from the DB
        or via '_kvec_get_vector' calls.  For now this is the same as for inline stores, but
        we might change that down the road to deal with the potentially lossy dtype inference,
        in case a vector is passed through an intermediary function call.
        """
        return self.get_optimized_code_inline()
        
    def get_code(self):
        if self.code is None:
            if self.optimize:
                # we can and should produce an optimized call:
                if isinstance(self.xstore, InlineVectorStore):
                    self.code = self.get_optimized_code_inline()
                    # embellish the name for the benefit of --debug:
                    self.name += '_inline'
                # this case is currently only used if the two array stores are of the same type,
                # even though they would also work for a mix of numpy and hd5 stores:
                else:
                    self.code = self.get_optimized_code_array_v2()
                    self.name += '_array_v2'
            else:
                self.code = self.get_generic_code()
                self.name += '_generic'
        return self.code

DotProduct('kvec_dot', num_params=2, deterministic=True).define()
DotProduct('kvec_dot_product', num_params=2, deterministic=True).define()


class CosineSimilarity(DotProduct):
    """Compute cosine similarity between two vectors x and y.
    Use faster dot-product if both vectors are appropriately normalized.
    """

    def have_l2_normalized_vectors(self):
        """Return True if both vectors are L2-normalized.
        """
        xnorm = self.xstore.get_vector_norm() if self.xstore is not None else False
        ynorm = self.ystore.get_vector_norm() if self.ystore is not None else False
        return xnorm == ispec.VectorIndex.NORM_L2 and ynorm == ispec.VectorIndex.NORM_L2

    def have_unnormalized_vectors(self):
        """Return True if neither vector is (known to be) normalized.
        """
        xnorm = self.xstore.get_vector_norm() if self.xstore is not None else False
        ynorm = self.ystore.get_vector_norm() if self.ystore is not None else False
        return not xnorm and not ynorm

    def translate_call_to_sql(self, query, expr, state):
        if len(expr.args) != 2:
            raise KGTKException(f"Illegal number of arguments to '{self.get_name()}'")
        self.xstore, _ = self.get_argument_vector_store(query, expr.args[0], state)
        self.ystore, _ = self.get_argument_vector_store(query, expr.args[1], state)
        if self.have_l2_normalized_vectors():
            # both vectors are normalized with L2, which means we can simply run
            # the dot product and we should produce an optimized translation:
            return self.translate_two_arg_call_to_optimized_sql(query, expr, state)
        else:
            return self.translate_two_arg_call_to_generic_sql(query, expr, state)

    def get_generic_unnormalized_vector_code(self):
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        def _cosine_similarity(x, y):
            # 'frombuffer' calls are very fast, O(1):
            vx = np.frombuffer(x, dtype=xdtype)
            vy = np.frombuffer(y, dtype=ydtype)
            norm = np.linalg.norm(vx) * np.linalg.norm(vy)
            # make sure we don't return numpy floats:
            return float(np.dot(vx, vy) / norm)
        return _cosine_similarity
    
    def get_code(self):
        if self.code is None:
            if self.have_l2_normalized_vectors():
                # both vectors are normalized with L2, simply run dot product,
                # we adapt the name for the benefit of --debug:
                self.name = 'kvec_dot_product'
                self.code = super().get_code()
            elif self.have_unnormalized_vectors():
                # neither vector is (known to be) normalized:
                self.code = self.get_generic_unnormalized_vector_code()
            else:
                raise KGTKException(f"cannot yet handle non-L2 or mix of norms in call to '{self.get_name()}'")
        return self.code

CosineSimilarity('kvec_cos_sim', num_params=2, deterministic=True).define()
CosineSimilarity('kvec_cosine_similarity', num_params=2, deterministic=True).define()


class TopKCosineSimilarity(VirtualGraphFunction, VectorFunction):
    """Find the top-k vectors with highest cosine similarity to a source vector.
    Requires the availability of an appropriate nearest-neighbor index on the
    associated vector store.
    """

    # input parameters needed by the 'VirtualTableFunction' API:
    params = ['node1',       # input vector for which we want to compute top-k similars
              'key',         # optional: node1 key associated with that vector (from the vector table)
              'k',           # optional: top-k similar nodes will be computed, defaults to 10
              'maxk',        # optional: maximum k to try for vector joins with dynamic scaling,
                             # defaults to 0 which means no dynamic scaling should be used
              'nprobe',      # optional: number of closest qcells to search to find neighbors, defaults to 1
              'batch_size',  # optional: input vector batch size to use to compute top-k similars,
                             # defaults to 1, if this is greater than 1 and no dynamic scaling is used, this
                             # will search batches of vectors which will greatly increase parallelism and speed
              'ntotal'       # optional: if batching is used, this must provide the exact total of inputs that
                             # need to be processed, needed to ensure proper processing of last batch
    ]
    # output parameters/columns that will be bound:
    columns = ['out_node1',  # respective input vector associated with neighbors needed for batched processing
               'out_key',    # respective input vector key associated with neighbors needed for batched processing
               'label',      # name of virtual edge (constant)
               'node2',      # node1 key of this similar vector
               'vid',        # edge ID of this similar vector
               'vrowid',     # row ID of this similar vector
               'vector',     # bytes of this similar vector
               'similarity'  # cosine similarity of this similar vector to the respective input vector
    ]
    name = 'kvec_topk_cosine_similarity'

    DEFAULT_K = 10
    DEFAULT_MAXK = 0
    DEFAULT_NPROBE = -1    # if <= 0, use the default from the NN-index
    DEFAULT_BATCH_SIZE = 1

    @staticmethod
    def initialize(vtfun, node1, key=None, k=DEFAULT_K, maxk=DEFAULT_MAXK, nprobe=DEFAULT_NPROBE,
                   batch_size=DEFAULT_BATCH_SIZE, ntotal=None):
        """Called during the initialziation of the virtual table function for a set of input
        parameters 'node1' (the source vector we are comparing against), 'k' (how many top-similar
        results to compute), and 'nprobe' (how deeply to search in the nearest-neighbor index).
        If 'maxk' is non-zero, 'k' will dynamically scale all the way to 'maxk' which is only
        useful, however, in conjunction with a similarity join controller.
        """
        vtfun.input_vector = node1
        vtfun.input_vector_key = key
        vtfun.input_k = k
        vtfun.input_maxk = maxk
        vtfun.input_nprobe = nprobe
        vtfun.batch_size = batch_size
        vtfun.ntotal = int(ntotal) if ntotal is not None else None
        vtfun.current_k = vtfun.input_k
        vtfun.search_index = None
        vtfun.result_rows = None
        vtfun.result_rows_offset = 0

        # additional slots needed to support full similarity joins via join controllers:
        # VERY TRICKY: the object actually running the result computation and iteration will be an
        # instance of this class created during registration with the DB connection, so we record
        # that here on the class so the join controller mechanism can access it from the class object
        # (each invocation creates its own class object, so we "should" have a 1-1 correspondence):
        type(vtfun).vtfun_impl = vtfun
        vtfun.top_k_values = None
        vtfun.debug = False
        if vtfun.debug:
            print('kvec_cos_sim_topk.init:')

        # TO DO: for now we only support batching without dynamic scaling, we'll need to generalize that,
        # but this is tricky, since each vector in the input group will behave and converge differently:
        vtfun.use_batching = batch_size > 1 and ntotal is not None and maxk == 0
        if vtfun.use_batching and not hasattr(vtfun, 'batched_inputs'):
            vtfun.nprocessed = 0
            vtfun.batched_inputs = []

    def supports_sim_join(self):
        """Signal that this computation supports full similarity joins via auxiliary join controllers."""
        return True

    @staticmethod
    def iterate(vtfun, idx):
        """Called by the virtual table function API when a new set of output values is requested.
        In our adaptation here, this static method becomes the implementation of TableFunction.iterate()
        on the dynamic class we create in self.get_code() below.  This just calls out to
        'vtfun.compute_result_rows()' and should generally not require any specialization on subclasses.
        """
        if vtfun.result_rows is None:
            if vtfun.use_batching:
                vtfun.batched_inputs.append((vtfun.input_vector, vtfun.input_vector_key))
                vtfun.nprocessed += 1
                if len(vtfun.batched_inputs) >= vtfun.batch_size or vtfun.nprocessed >= vtfun.ntotal:
                    vtfun.result_rows = vtfun.compute_result_rows()
                    vtfun.batched_inputs = []
                else:
                    vtfun.search_index = None # unlink this
                    raise StopIteration
            else:
                vtfun.result_rows = vtfun.compute_result_rows()
        try:
            row = next(vtfun.result_rows)
        except StopIteration:
            if vtfun.current_k < vtfun.input_maxk:
                vtfun.current_k = min(vtfun.current_k * 2, vtfun.input_maxk)
                # TO DO: make follow-up calls with larger k more efficient, reintroduce vector caching
                vtfun.result_rows = vtfun.compute_result_rows()
                row = next(vtfun.result_rows)
            else:
                vtfun.search_index = None # unlink this
                raise StopIteration
        if vtfun.debug:
            print('kvec_cos_sim_topk.next:', row[1])
        vtfun.result_rows_offset += 1
        return row

    @staticmethod
    def compute_result_rows(vtfun):
        """Called to compute a set of 'k' result rows for the set of input parameters stored by 'initialize'.
        Each row binds all output 'columns' specified above.  If no nearest-neighbor index is available
        for the associated vector store, this simply fails with an empty result.
        """
        if vtfun.use_batching:
            vectors = [i[0] for i in vtfun.batched_inputs]
            keys = [i[1] for i in vtfun.batched_inputs]
        else:
            vectors = [vtfun.input_vector]
            keys = [vtfun.input_vector_key]
        vstore = vtfun.vector_store
        nnindex = vstore.get_nearest_neighbor_index() if vstore is not None else None
        if not nnindex or not nnindex.is_trained():
            #return iter([])
            # don't silently fail, since this is most likely an error or oversight:
            raise KGTKException(f"no trained nearest neighbor index available for '{vtfun.name}'")
        k = vtfun.current_k
        nprobe = vtfun.input_nprobe if vtfun.input_nprobe > 0 else nnindex.nprobe
        ndim = vstore.get_vector_ndim()
        dtype = vstore.get_vector_dtype()
        vectors = [np.frombuffer(vector, dtype=dtype) for vector in vectors]
        vectors = np.vstack(vectors)
        # TO DO: reconsider caching this index here, since it creates a potential memory leak
        # and we might not need to do that anymore now that search index reuse is working:
        if vtfun.search_index is None:
            # first time around, create the FAISS search index for the respective qcells;
            # we will reuse that if we do dynamic scaling towards maxk:
            vtfun.search_index = nnindex.get_search_index_for_vectors(vectors, nprobe=nprobe)
        # TO DO: possibly increase 'k' here to account for different L2 vs. cosine distance ordering
        # (e.g., in query manual data with '(x:Q913)...(xv)-[r:kvec_topk_cos_sim {k: 5}]->(y) vs. k=6):
        D, V = nnindex.search(vectors, k, nprobe=nprobe, index=vtfun.search_index)
        
        # for batched processing, we might get O(10000) input vectors with k neighbors for each of them;
        # to get the best possible locality when we access their information with 'get_vector_rows_by_id',
        # we sort all neighbor vectors by their numeric ID which is a rowid to the vector table; however,
        # that introduces a bit of extra complexity to associate NN-vector IDs with the ID of the input
        # vector in the current batch they are a neighbor to:
        results = []
        label = TopKCosineSimilarity.name
        # build a set of (NN-vector-ID, input-vector-ID) tuples over all search results:
        nn_indexed_ids = [ (vid, i) for i, row in enumerate(V[:,vtfun.result_rows_offset:]) for vid in row ]
        # sort NN-vector IDs numerically:
        nn_indexed_ids.sort(key=lambda x: x[0])
        nn_ids = [x[0] for x in nn_indexed_ids]
        # this creates a 32-bit norm which changes our results when comparing to prior runs:
        #vxnorms = np.linalg.norm(vectors , axis=1)
        vxnorms = [np.linalg.norm(vx) for vx in vectors]
        vxbytes = [vx.tobytes() for vx in vectors]
        for row, (vid, i) in zip(vstore.get_vector_rows_by_id(nn_ids), nn_indexed_ids):
            vx = vectors[i]
            vxnorm = vxnorms[i]
            vxbyte = vxbytes[i]
            vxkey = keys[i]
            vy = row[4]
            # [vxi, 'out_node1', 'out_key', 'label', 'node2', 'vid', 'vrowid', 'vector', 'similarity']
            res = [i, vxbyte, vxkey, label, row[1], row[0], row[3], vy.tobytes(), 0.0]
            vynorm = np.linalg.norm(vy)
            # make sure we don't return numpy floats:
            sim = float(np.dot(vx, vy) / (vxnorm * vynorm))
            res[-1] = sim
            results.append(res)
        # sort each result group, first by similarity:
        results.sort(key=lambda x: x[-1], reverse=True)
        # then by input batch vector ID:
        results.sort(key=lambda x: x[0])
        # now cut out auxiliary input batch vector IDs:
        results = [res[1:] for res in results]
        return iter(results)

    # see .old/funcvec.py.4 if we need to compare with old runs:
    #def compute_result_rows_v1(vtfun):

    def get_code(self):
        """Create the virtual table code object and associate the appropriate vector store
        as determined by self.translate_call_to_sql().
        """
        if self.code is None:
            super().get_code()
            self.code.vector_store = self.xstore
        return self.code

    def has_join_controller(self, query, clause, state):
        """Return True if a similarity join controller linked to this 'clause'
        has already been added to 'query'.
        """
        rel = clause[1]
        vrel = rel.variable
        for mclause in query.get_top_level_match_clauses():
            for pclause in mclause.get_pattern_clauses():
                prel = pclause[1]
                # test if we have a join controller clause that matches on the variable:
                if prel.variable.name == vrel.name and prel.labels == ('kvec_sim_join_controller',):
                    return True
        return False

    def add_join_controller(self, query, clause, state):
        """Add a similarity join controller linked to this 'clause'
        so we can do dynamic scaling for this similarity query.
        """
        # this is a little low level, we need some better abstractions if we do this more often:
        node1, rel, node2 = clause
        vrel = rel.variable
        vnode2 = node2.variable
        # getting a usable graph handle is a little crufty - it would be nice to have
        # a syntax that would let us reference a graph table such as 'graph_4' directly:
        graph = node1.graph.name if node1.graph else query.default_graph
        # we start with the optional join controller match clause in surface syntax:
        cont_clause = f'`{graph}`: (`{vnode2.name}`)-[`{vrel.name}`:kvec_sim_join_controller]->()'
        parser_query = query.query
        # we need to wrap it into a dummy top-level query that is valid Kypher to parse it:
        qtree = parser.parse(f'MATCH ()-[]->() OPTIONAL MATCH {cont_clause} RETURN *')
        # now we excise the parsed optional clause tree we want:
        opt_clause = qtree[1][2]
        # intern and simplify it into the parsed query of this query:
        opt_clause = parser.intern_ast(parser_query, opt_clause).simplify()
        # add the new optional clause to the end:
        parser_query.get_optional_match_clauses().append(opt_clause)
        # also update optional clauses of the top-level query object:
        query.optional_clauses = parser_query.get_optional_match_clauses()

    def translate_call_to_sql(self, query, clause, state):
        """Called by query.pattern_clause_to_sql() to translate a clause
        with a virtual graph pattern.  This primarily computes the associated
        vector store and forces 'dont_optimize'.
        """
        node1 = clause[0]
        rel = clause[1]
        if rel.labels is None:
            return

        # supply default arguments - this isn't strictly necessary anymore and seems
        # to be working now, but leaving inputs unbound does affect the cost estimate
        # to the query optimizer which we can address in the new version of TableFunction;
        # we disable this for now, but we might have to reinstate it if problems occur:
        rel.properties = rel.properties or {}
        #rel.properties.setdefault('k', parser.Literal(query.query, self.DEFAULT_K))
        #rel.properties.setdefault('maxk', parser.Literal(query.query, self.DEFAULT_MAXK))
        #rel.properties.setdefault('nprobe', parser.Literal(query.query, self.DEFAULT_NPROBE))

        # maxk != 0 means dynamic scaling which needs a join controller which we add here on demand.
        # NOTE: if maxk points to a variable for some reason, we'll add a controller regardless:
        maxk = rel.properties.get('maxk')
        maxk = maxk.value if isinstance(maxk, parser.Literal) else maxk
        if maxk is not None and maxk != self.DEFAULT_MAXK and not self.has_join_controller(query, clause, state):
            self.add_join_controller(query, clause, state)
            # abort current translation to top level and restart:
            query.retranslate()
            
        if 'batch_size' in rel.properties and not all(map(lambda k: k in rel.properties, ('ntotal', 'key', 'out_key'))):
            # enforce this for now to avoid surprises:
            raise KGTKException(f"{self.name}: 'batch_size' also requires 'ntotal', 'key' and 'out_key' parameters")
        
        # we force dont_optimize for match clauses containing this virtual graph:
        query.get_pattern_clause_match_clause(clause).dont_optimize = True
        
        # compute relevant vector store:
        self.xstore, _ = self.get_argument_vector_store(query, node1.variable, state, clause=clause)
        # now finish translation with standard translator:
        super().translate_call_to_sql(query, clause, state)

TopKCosineSimilarity('kvec_topk_cos_sim').define()
TopKCosineSimilarity('kvec_topk_cosine_similarity').define()

"""
# Example query:
> kgtk query --gc wikidata-20210215-dwd-v2-embeddings-test.sqlite3.db -i complexemb -i labels \
       --match 'comp: (x:Q40)-[]->(xv), \
                      (xv)-[r:kvec_topk_cos_sim {k: 20, nprobe: 8}]->(y), \
                lab:  (x)-[]->(xl), (y)-[]->(yl)' \
       --where 'x != y' \
       --return 'x, xl, y, yl, r.similarity' \
       --limit 10
node1	node2	node2	node2	similarity
Q40	'Austria'@en	Q28	'Hungary'@en	0.7745946049690247
Q40	'Austria'@en	Q794	'Iran'@en	0.7634432315826416
Q40	'Austria'@en	Q347	'Liechtenstein'@en	0.7329589128494263
Q40	'Austria'@en	Q155	'Brazil'@en	0.7318835854530334
Q40	'Austria'@en	Q79	'Egypt'@en	0.7268905639648438
Q40	'Austria'@en	Q35	'Denmark'@en	0.7170709371566772
Q40	'Austria'@en	Q212	'Ukraine'@en	0.7160522937774658
Q40	'Austria'@en	Q865	'Taiwan'@en	0.7146331071853638
Q40	'Austria'@en	Q928	'Philippines'@en	0.7101161479949951
Q40	'Austria'@en	Q298	'Chile'@en	0.7095608711242676
"""


### Join controllers to support full similarity joins:

# The winning incantation seems to be to use an optional clause with
# SimilarityJoinController and in addition do a dont-optimize on the
# match clause containing the similarity computation - we might
# (eventually) be able to only enclose the vtable computation in cross
# joins instead of doing it for all clauses, but for now the whole
# match clause will be deoptimized (see 'TopKCosineSimilarity').

# TO DO: once we are confident that this is the right way to go,
# these controllers should be inserted automatically into the query

class SimilarityJoinController(VirtualGraphFunction):
    """Virtual graph helper function that assists a similarity function such as
    'kvec_topk_cos_sim' to compute full similarity joins.  The basic idea is to
    insert this dummy computation at a point in the query where all the relevant
    restrictions on a candidate similarity element have been tested (that is
    the candidate qualifies for output), and that candidate then becomes an input
    to this virtual graph computation.  We then record it as a result and shortcut
    the main similarity computation if enough results have been computed.

    Finding the right spot for insertion to do what we want it to do in the nested
    loop join carried out by SQLite is tricky.  So far the winning combination seems
    to be to insert this in an optional clause following the main sim computation
    and pattern, and (optionally) use a cross join in the main pattern to avoid
    any surprises from query optimization.  For example, something like this works
    (the explicit use of 'maxk' indicates that we want to dynamically grow the set
    of computed candidates until we found enough qualifying for the join, the
    relation variable 'r' links the two clauses):

        kgtk query --gc ... --ac ...
             -i short_abstracts_textemb -i labels -i claims \
             --match 'emb:      (x)-[]->(xv), \
                                (xv)-[r:kvec_topk_cos_sim {k: 8, maxk: 1024, nprobe: 4}]->(y), \
                      claims:   (y)-[:P106]->(:Q4964182), \
                                (y)-[:P31]->(:Q5), \
                      labels:   (x)-[]->(xl), \
                      labels:   (y)-[]->(yl)' \
             --where 'x in ["Q859", "Q868", "Q913"] and x != y' \
             --opt   'emb:      (y)-[r:kvec_sim_join_controller]->()' \
             --return 'xl as xlabel, r.similarity as sim, yl as ylabel'

    Once we are confident this is the way to go, we can insert these auxiliary clauses
    automatically during translation of 'kvec_topk_cos_sim' and others.
    """

    # parameters needed by the 'VirtualTableFunction' API:
    params = ['node1', 'k']
    columns = ['label', 'node2']

    # the default value of 0 means to use the 'k' from the main sim computation:
    DEFAULT_K = 0

    @staticmethod
    def initialize(vtfun, node1, k=DEFAULT_K):
        """Initialize a call to the virtual graph function 'vtfun'.  If 'k' == 0,
        use the 'k' of the associated main similarity function computation.
        """
        vtfun.input_node1 = node1
        vtfun.input_k = int(k)
        vtfun.result_rows = None
        # points to the similarity function code object that is controlled by this controller
        # (the proper linkage is established during self.translate_call_to_sql() below):
        vtfun.sim_function = type(vtfun).sim_function.code.vtfun_impl
        if vtfun.sim_function.top_k_values is None:
            vtfun.sim_function.top_k_values = set()

    @staticmethod
    def compute_result_rows(vtfun):
        """Receives one similarity candidate as input/node1 that satisfies all join conditions,
        registers it and performs any resetting of the main similarity computation if necessary,
        and returns a dummy result so this computation always succeeds.
        """
        value = vtfun.input_node1
        k = vtfun.input_k
        # from now on we are operating within the virtual function of the sim computation:
        vtfun = vtfun.sim_function
        # if k == 0, default to the 'k' of the similarity computation:
        k = k or vtfun.input_k
        if vtfun.debug:
            print('topk_values_vtable:', value)
        vtfun.top_k_values.add(value)
        if len(vtfun.top_k_values) >= k:
            # we generated 'k' fully qualifying similar nodes for the
            # sim function's 'input_node1', terminate its iteration:
            if vtfun.debug:
                print('topk_values_vtable: reset', vtfun.current_k)
            vtfun.result_rows = iter([])
            vtfun.top_k_values.clear()
            vtfun.input_maxk = 0
        # return a dummy identity result:
        return iter([['label', value]])

    @staticmethod
    def get_sim_function(query, vrel, state):
        """Find a qualifying similarity function linked to this controller via 'vrel'.
        Return None if nothing could be found.
        """
        for mclause in query.get_top_level_match_clauses():
            for pclause in mclause.get_pattern_clauses():
                prel = pclause[1]
                # test variable name match, but ensure that the variable is from a different clause:
                if prel.variable.name == vrel.name and prel.variable is not vrel:
                    # we found a pattern clause whose relation var matches the vrel variable here:
                    vgraph = query.get_pattern_clause_graph(pclause)
                    sim_function = state.lookup_vtable(vgraph)
                    if hasattr(sim_function, 'supports_sim_join') and sim_function.supports_sim_join():
                        return sim_function
        return None
    
    def translate_call_to_sql(self, query, clause, state):
        """Called by query.pattern_clause_to_sql() to translate a clause
        with a virtual graph pattern.  This additionally links to the
        corresponding similarity function and supplies property defaults.
        """
        rel = clause[1]
        self.sim_function = self.get_sim_function(query, rel.variable, state)
        if not self.sim_function:
            raise KGTKException(f"{self.name}: failed to find base similarity function")
        # avoid creating a join between the two vtables:
        rel.variable = query.query.create_anonymous_variable()

        # supply default arguments - this isn't strictly necessary anymore and seems
        # to be working now, but leaving inputs unbound does affect the cost estimate
        # to the query optimizer which we can address in the new version of TableFunction,
        # but until that's available, we leave this as is:
        rel.properties = rel.properties or {}
        rel.properties.setdefault('k', parser.Literal(query.query, self.DEFAULT_K))

        super().translate_call_to_sql(query, clause, state)
        # link the uniquified code object to the virtual graph function we computed above:
        self.get_code().sim_function = self.sim_function
        
SimilarityJoinController('kvec_sim_join_controller').define()


class SimilarityJoinControllerFunction(VectorFunction):
    """Function version of 'SimilarityJoinController' (which see), which can be used
    in where clauses or return expressions.  Controlling the exact application of this
    function without unexpected interference from the query optimizer seems more difficult,
    however, which was the reason for the vtable version in the first place.  Here is a
    working invocation (the first arg links to the base similarity computation, the second
    arg controls how many values to return, and the third argument will be registered upon
    each call; additional otherwise unused args can be used to introduce clause dependencies):

        kgtk query --gc ... --ac ... \
             -i short_abstracts_textemb -i labels -i claims \
             --match 'emb:      (x)-[]->(xv), \
                                (xv)-[r:kvec_topk_cos_sim {k: 5, nprobe: 4}]->(y), \
                      claims:   (y)-[:P31]->(:Q5), \
                      labels:   (x)-[]->(xl), (y)-[]->(yl)' \
             --where 'x in ["Q859", "Q868", "Q913"] and x != y' \
             --return 'xl as xlabel, r.similarity as sim, yl as ylabel, kvec_sim_join_ctrl(r, 2, yl) as yl2'
    """

    def translate_call_to_sql(self, query, expr, state):
        """Does some minimal argument checking and translates the call to SQL.
        This additionally links to the corresponding similarity function.
        """
        if len(expr.args) >= 3:
            vrel = expr.args[0]
            self.sim_function = SimilarityJoinController.get_sim_function(query, vrel, state)
            if not self.sim_function:
                raise KGTKException(f"{self.name}: failed to find base similarity function")
            # cut out vrel variable which is only needed for translation:
            expr.args = expr.args[1:]
            return super().translate_call_to_sql(query, expr, state)
        else:
            raise KGTKException(f"{self.name}: illegal call arguments")

    def get_code(self):
        if self.code is None:
            sim_function = self.sim_function.code
            
            def _join_controller(k, value, *deps):
                # access the code object of the sim function:
                vtfun = sim_function.vtfun_impl
                if vtfun.debug:
                    print('kvec_sim_join_ctrl:', value)
                if vtfun.top_k_values is None:
                    vtfun.top_k_values = set()
                vtfun.top_k_values.add(value)
                if len(vtfun.top_k_values) >= k:
                    # we generated 'k' fully qualifying similar nodes for the
                    # sim function's 'input_node1', terminate its iteration:
                    if vtfun.debug:
                        print('kvec_sim_join_ctrl: reset', vtfun.current_k)
                    vtfun.result_rows = iter([])
                    vtfun.top_k_values.clear()
                    vtfun.input_maxk = 0
                # return a dummy identity result:
                return value
            
            self.code = _join_controller
        return self.code

SimilarityJoinControllerFunction(name='kvec_sim_join_ctrl', deterministic=True).define()


### Vector computations:

class EuclideanDistance(GenericVectorFunction):
    """Compute the Euclidean distance between two vectors.
    """
    
    def get_generic_code(self):
        """Generic calls assume byte strings as inputs which either come directly from the DB
        or via '_kvec_get_vector' calls.
        """
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        def _euclidean_distance(x, y):
            # 'frombuffer' calls are very fast, O(1):
            vx = np.frombuffer(x, dtype=xdtype)
            vy = np.frombuffer(y, dtype=ydtype)
            # make sure we don't return numpy floats:
            return float(np.linalg.norm(vx - vy))
        return _euclidean_distance

EuclideanDistance('kvec_euclidean_distance', num_params=2, deterministic=True).define()
EuclideanDistance('kvec_euclid_dist', num_params=2, deterministic=True).define()


class L0Norm(GenericVectorFunction):
    """Compute the L0-Norm of a vector ('numpy.linalg.norm(x, ord=0)').
    Counts the number of non-zero elements in a vector.
    """
    
    def get_generic_code(self):
        """Generic calls assume byte strings as inputs which either come directly from the DB
        or via '_kvec_get_vector' calls.
        """
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        def _l0_norm(x):
            # 'frombuffer' calls are very fast, O(1):
            vx = np.frombuffer(x, dtype=xdtype)
            # make sure we don't return numpy floats:
            return float(np.linalg.norm(vx, ord=0))
        return _l0_norm

L0Norm('kvec_l0_norm', num_params=1, deterministic=True).define()


class L1Norm(GenericVectorFunction):
    """Compute the L1-Norm of a vector ('numpy.linalg.norm(x, ord=1)').
    Counts the sum of dimensions of a vector (Manhattan distance).
    """
    
    def get_generic_code(self):
        """Generic calls assume byte strings as inputs which either come directly from the DB
        or via '_kvec_get_vector' calls.
        """
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        def _l1_norm(x):
            # 'frombuffer' calls are very fast, O(1):
            vx = np.frombuffer(x, dtype=xdtype)
            # make sure we don't return numpy floats:
            return float(np.linalg.norm(vx, ord=1))
        return _l1_norm

L1Norm('kvec_l1_norm', num_params=1, deterministic=True).define()


class L2Norm(GenericVectorFunction):
    """Compute the L2-Norm or Euclidean norm or Euclidean length of a vector
    ('numpy.linalg.norm(x, ord=2)').
    """
    
    def get_generic_code(self):
        """Generic calls assume byte strings as inputs which either come directly from the DB
        or via '_kvec_get_vector' calls.
        """
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        def _l2_norm(x):
            # 'frombuffer' calls are very fast, O(1):
            vx = np.frombuffer(x, dtype=xdtype)
            # make sure we don't return numpy floats:
            return float(np.linalg.norm(vx, ord=2))
        return _l2_norm

L2Norm('kvec_l2_norm', num_params=1, deterministic=True).define()


# TO DO:
# The computations below can produce new vectors as their results.  For now - for simplicity -
# we force those vectors to be of dtype VectorFunction.DEFAULT_DTYPE, since that is the vector
# data type assumed for arguments that are not associated with any vector store.  In the future
# we could compute the result type of such a function call statically at translation time, and
# then pass that type to functions taking such an argument similar to what we do for vector args
# associated with a vector store/table where we know the dtype.

class VectorPlus(GenericVectorFunction):
    """Compute elementwise addition 'x + y' between two vectors and/or numbers ('numpy.add').
    If at least one argument is a vector, the result will also be a vector.
    """
    
    def get_generic_code(self):
        """Generic calls assume byte strings as inputs which either come directly from the DB
        or via '_kvec_get_vector' calls.
        """
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        # type enforced for newly created vectors - see note above:
        result_dtype = self.DEFAULT_DTYPE
        def _vector_plus(x, y):
            # 'frombuffer' calls are very fast, O(1):
            x = np.frombuffer(x, dtype=xdtype) if isinstance(x, bytes) else x
            y = np.frombuffer(y, dtype=ydtype) if isinstance(y, bytes) else y
            result = x + y
            return result.astype(result_dtype).tobytes() if isinstance(result, np.ndarray) else result
        return _vector_plus

VectorPlus('kvec_plus', num_params=2, deterministic=True).define()


class VectorMinus(GenericVectorFunction):
    """Compute elementwise subtraction 'x - y' between two vectors and/or numbers ('numpy.subtract').
    If at least one argument is a vector, the result will also be a vector.
    """
    
    def get_generic_code(self):
        """Generic calls assume byte strings as inputs which either come directly from the DB
        or via '_kvec_get_vector' calls.
        """
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        result_dtype = self.DEFAULT_DTYPE
        def _vector_minus(x, y):
            # 'frombuffer' calls are very fast, O(1):
            x = np.frombuffer(x, dtype=xdtype) if isinstance(x, bytes) else x
            y = np.frombuffer(y, dtype=ydtype) if isinstance(y, bytes) else y
            result = x - y
            return result.astype(result_dtype).tobytes() if isinstance(result, np.ndarray) else result
        return _vector_minus

VectorMinus('kvec_minus', num_params=2, deterministic=True).define()


class VectorTimes(GenericVectorFunction):
    """Compute elementwise multiplication 'x * y' between two vectors and/or numbers ('numpy.multiply').
    If at least one argument is a vector, the result will also be a vector.
    """
    
    def get_generic_code(self):
        """Generic calls assume byte strings as inputs which either come directly from the DB
        or via '_kvec_get_vector' calls.
        """
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        result_dtype = self.DEFAULT_DTYPE
        def _vector_times(x, y):
            # 'frombuffer' calls are very fast, O(1):
            x = np.frombuffer(x, dtype=xdtype) if isinstance(x, bytes) else x
            y = np.frombuffer(y, dtype=ydtype) if isinstance(y, bytes) else y
            result = x * y
            return result.astype(result_dtype).tobytes() if isinstance(result, np.ndarray) else result
        return _vector_times

VectorTimes('kvec_times', num_params=2, deterministic=True).define()


class VectorDivide(GenericVectorFunction):
    """Compute elementwise division 'x / y' between two vectors and/or numbers ('numpy.divide').
    If at least one argument is a vector, the result will also be a vector.
    """
    
    def get_generic_code(self):
        """Generic calls assume byte strings as inputs which either come directly from the DB
        or via '_kvec_get_vector' calls.
        """
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        result_dtype = self.DEFAULT_DTYPE
        def _vector_divide(x, y):
            # 'frombuffer' calls are very fast, O(1):
            x = np.frombuffer(x, dtype=xdtype) if isinstance(x, bytes) else x
            y = np.frombuffer(y, dtype=ydtype) if isinstance(y, bytes) else y
            result = x / y
            return result.astype(result_dtype).tobytes() if isinstance(result, np.ndarray) else result
        return _vector_divide

VectorDivide('kvec_divide', num_params=2, deterministic=True).define()


### Input/output:

# TO DO: implement more general and efficient 'kvec_to_text' and 'kvec_from_text' converters;
#        in general, generating and parsing floats is slow, so byte-IO is always preferred

class VectorStringify(GenericVectorFunction):
    """Convert a vector into text format as a KGTK string.  Calls 'kgtk_stringify' for non-vectors.
    """
    
    def get_generic_code(self):
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        precision = xdtype.itemsize * 2 # 2 digits per byte
        kgtk_stringify = self.get_function('kgtk_stringify').get_code()
        
        def _vector_stringify(x):
            if isinstance(x, bytes):
                x = np.frombuffer(x, dtype=xdtype)
                # formatting floats to text seems to be slow in Python and NumPy, no matter what we try:
                # this seems to be at the core of it all in NumPy with an insane number of options:
                #xtext = np.array2string(x, separator=',', precision=precision, max_line_width=1000000000)
                # 1.5 times the speed but produces larger files since we have no precision control:
                #xtext = str(x.tolist())
                # twice the speed of array2string - about 5.5 min for 1M 100-D vectors:
                ffmt = f'.{precision}g'
                xtext = ','.join(map(lambda x: format(x, ffmt), x))
                # same as format:
                #xtext = ','.join(map(lambda x: f'{x:.8g}', x))
                return '"[' + xtext + ']"'
            return kgtk_stringify(x)
        return _vector_stringify

VectorStringify('kvec_stringify', num_params=1, deterministic=True).define()


class VectorUnstringify(GenericVectorFunction):
    """Convert a vector from text format to vector bytes.  Return 'x' for non-vector strings.
    """
    
    def get_generic_code(self):
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        result_dtype = self.DEFAULT_DTYPE
        separators = (',', ';', ':', '|', ' ')
        
        def _vector_unstringify(x):
            if isinstance(x, str):
                start = 0
                if x.startswith('"'):
                    start += 1
                if x.startswith('[', start):
                    start += 1
                end = -start if start > 0 else None
                x = x[start:end]
                # auto-guess a separator:
                for sep in separators:
                    if sep in x:
                        return np.fromstring(x, dtype=result_dtype, sep=sep).tobytes()
                else:
                    # try to handle vectors of length <= 1:
                    return np.fromstring(x, dtype=result_dtype, sep=',').tobytes()
            return x
        return _vector_unstringify

VectorUnstringify('kvec_unstringify', num_params=1, deterministic=True).define()


class VectorToBase64(GenericVectorFunction):
    """Convert a vector into base64 format wrapped as a KGTK string.  Returns null for non-vectors.
    An optional 'dtype' argument specifies the target element dtype before base64 conversion.
    """

    def translate_call_to_sql(self, query, expr, state):
        args = expr.args
        if len(args) == 1:
            # add a default value for dtype at translation time which is more efficient:
            args.append(parser.Literal(query.query, self.DEFAULT_DTYPE.name))
        return super().translate_call_to_sql(query, expr, state)
            
    def get_generic_code(self):
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        from base64 import standard_b64encode as b64encode
        
        def _vector_to_base64(x, dtype):
            if isinstance(x, bytes):
                if xdtype.name == dtype:
                    xbytes = x
                else:
                    # we need dtype conversion:
                    xbytes = np.frombuffer(x, dtype=xdtype).astype(dtype).tobytes()
                # this is about 8x faster than kvec_stringify:
                code = b64encode(xbytes).decode()
                return '"' + code + '"'
        return _vector_to_base64

VectorToBase64('kvec_to_base64', num_params=2, deterministic=True).define()


class VectorFromBase64(GenericVectorFunction):
    """Convert a vector from base64 format into vector bytes.  Returns null for non-vectors.
    An optional 'dtype' argument specifies the element dtype of the source vector 'x'.
    """
    
    def translate_call_to_sql(self, query, expr, state):
        args = expr.args
        if len(args) == 1:
            # add a default value for dtype at translation time which is more efficient:
            args.append(parser.Literal(query.query, self.DEFAULT_DTYPE.name))
        return super().translate_call_to_sql(query, expr, state)
    
    def get_generic_code(self):
        sstore, xtab, xcol, xdtype, xcache, ytab, ycol, ydtype, ycache = self.get_call_context()
        result_dtype = self.DEFAULT_DTYPE
        from base64 import standard_b64decode as b64decode
        
        def _vector_from_base64(x, dtype):
            if isinstance(x, str):
                if x.startswith('"'):
                    xbytes = b64decode(x[1:-1])
                else:
                    xbytes = b64decode(x)
                if result_dtype.name != dtype:
                    # we need dtype conversion:
                    xbytes = np.frombuffer(xbytes, dtype=dtype).astype(result_dtype).tobytes()
                return xbytes
        return _vector_from_base64

VectorFromBase64('kvec_from_base64', num_params=2, deterministic=True).define()
