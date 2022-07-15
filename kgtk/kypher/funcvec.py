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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uniquify = True
        self.xstore = None     # used to hold the vector store corresponding to the first x argument
        self.ystore = None     # used to hold the vector store corresponding to the second y argument
        self.optimize = False  # internal switch to flag whether to produce optimized or generic code

    def get_argument_vector_store(self, query, arg, state):
        """If 'arg' is a column variable that can be linked to a vector store,
        return the associated vector store object, otherwise return None.
        As the second return value, return the optimized reference that can
        be used for the vector for this type of vector store.
        """
        # TO DO: figure out whether we need to worry about join-variables here
        # that can't be linked unambiguously to a table, but then joins on 
        # vector columns don't really make sense, do they?
        if isinstance(arg, parser.Variable):
            graph, column, sql = query.variable_to_sql(arg, state)
            table = state.get_alias_table(graph)
            master = self.store.get_vector_store()
            if master.has_vector_store(table, column):
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
        xtable, xcolumn, xdtype = None, None, np.float32
        xcache = [None, None]
        if xstore is not None:
            xtable = xstore.table
            xcolumn = xstore.column
            xdtype = xstore.get_vector_dtype()
        ytable, ycolumn, ydtype = None, None, np.float32
        ycache = [None, None]
        if ystore is not None:
            ytable = ystore.table
            ycolumn = ystore.column
            ydtype = ystore.get_vector_dtype()
        return sql_store, xtable, xcolumn, xdtype, xcache, ytable, ycolumn, ydtype, ycache

    def translate_two_arg_call_to_optimized_sql(self, query, expr, state):
        args = expr.args
        if len(args) != 2:
            raise Exception("Illegal number of arguments to '{self.get_name()}'")
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
            raise Exception("Illegal number of arguments to '{self.get_name()}'")
        self.xstore, xref = self.get_argument_vector_store(query, args[0], state)
        self.ystore, yref = self.get_argument_vector_store(query, args[1], state)
        self.optimize = False
        # each arg is assumed to yield a byte-string encoding a vector:
        args = [query.expression_to_sql(arg, state) for arg in args]
        self.load()
        return f'{self.get_name()}({", ".join(args)})'


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
            raise Exception("Illegal number of arguments to '{self.get_name()}'")
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

    # parameters needed by the 'VirtualTableFunction' API:
    params = ['node1', 'k', 'nprobe']
    columns = ['label', 'node2', 'vid', 'vrowid', 'vector', 'similarity']
    name = 'kvec_topk_cosine_similarity'

    @staticmethod
    def initialize(vtfun, node1, k=10, nprobe=0):
        """Called during the initialziation of the virtual table function for a set of input
        parameters 'node1' (the source vector we are comparing against), 'k' (how many top-similar
        results to compute), and 'nprobe' (how deeply to search in the nearest-neighbor index).
        """
        # TO DO: the optional arguments don't work as expected, we always have to supply them it seems,
        #        otherwise the query breaks, figure out how to work around that...
        vtfun.input_vector = node1
        vtfun.input_k = k
        vtfun.input_nprobe = nprobe
        vtfun._result_rows = None

    @staticmethod
    def compute_result_rows(vtfun):
        """Called to compute a set of 'k' result rows for the set of input parameters stored by 'initialize'.
        Each row binds all output 'columns' specified above.  If no nearest-neighbor index is available
        for the associated vector store, this simply fails with an empty result.
        """
        vector = vtfun.input_vector
        k = vtfun.input_k
        nprobe = vtfun.input_nprobe
        vstore = vtfun.vector_store
        nnindex = vstore.get_nearest_neighbor_index() if vstore is not None else None
        if not nnindex or not nnindex.is_trained():
            return iter([])
        ndim = vstore.get_vector_ndim()
        dtype = vstore.get_vector_dtype()
        vector = np.frombuffer(vector, dtype=dtype)
        # TO DO: possibly increase 'k' here to account for different L2 vs. cosine distance ordering:
        D, V = nnindex.search(vector, k, nprobe=nprobe)
        result = []
        label = TopKCosineSimilarity.name
        vx = vector
        vxnorm = np.linalg.norm(vx)
        for row in vstore.get_vector_rows_by_id(V[0]):
            vy = row[4]
            # ['label', 'node2', 'vid', 'vrowid', 'vector', 'similarity']
            res = [label, row[1], row[0], row[3], vy.tobytes(), 0.0]
            vynorm = np.linalg.norm(vy)
            # make sure we don't return numpy floats:
            sim = float(np.dot(vx, vy) / (vxnorm * vynorm))
            res[-1] = sim
            result.append(res)
        result.sort(key=lambda x: x[-1], reverse=True)
        return iter(result)

    def get_code(self):
        """Create the virtual table code object and associate the appropriate vector store
        as determined by self.translate_call_to_sql().
        """
        if self.code is None:
            super().get_code()
            self.code.vector_store = self.xstore
        return self.code

    def translate_call_to_sql(self, query, clause, state):
        """Called by query.pattern_clause_to_sql() to translate a clause
        with a virtual graph pattern.  This primarily substitutes the
        appropriate virtual graph tables to use and computes the associated
        vector store.
        """
        node1 = clause[0]
        rel = clause[1]
        if rel.labels is None:
            return
        self.xstore, _ = self.get_argument_vector_store(query, node1.variable, state)
        # load here so we get the uniquified name registered with the connection:
        self.load()
        old_graph = node1._graph_table
        old_graph_alias = node1._graph_alias
        new_graph = self.get_name()
        # create a new alias (which is fine given we have a unique table name),
        # this will transparently handle qualified graph table names:
        new_graph_alias = state.get_table_aliases(new_graph, new_graph + '_c')[0]
        node1._graph_table = new_graph
        node1._graph_alias = new_graph_alias
        # TO DO: support this in query.py:
        #state.unregister_table_alias(old_graph, old_graph_alias)
        state.register_table_alias(new_graph, new_graph_alias)
        # prevent the generation of a label restriction based on the virtual graph name:
        rel.labels = None
        # now finish translation with standard translator:
        query.pattern_clause_to_sql(clause, new_graph_alias, state)

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
