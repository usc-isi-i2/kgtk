# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Query knowledge graphs and embeddings with KGTK Kypher-V

# Kypher-V supports import and queries over vector data. Kypher-V extends
# Kypher to allow work with unstructured data such as text, images, and so
# on, represented by embedding vectors. Kypher-V provides efficient storage,
# indexing and querying of large-scale vector data on a laptop. It is fully
# integrated into Kypher to enable expressive hybrid queries over
# Wikidata-size structured and unstructured data. To the best of our
# knowledge, this is the first system providing such a functionality in a
# query language for knowledge graphs.

# Please see the [**Kypher-V Manual**](https://kgtk.readthedocs.io/en/latest/transform/query/#kypher-v)
# for an introduction to the basic concepts and usage.


# <A NAME="setup"></A>
# ### Setup
#
# Some preliminaries to facilitate command invocation and result formatting:

# +
import re
from IPython.display import display, HTML
from kgtk.functions import kgtk

def show_html(img_width=150):
    """Display command output in 'out' as HTML after munging image links for inline display."""
    output = '\n'.join(out)
    html = re.sub(r'<td>&quot;(https?://upload.wikimedia.org/[^<]+)&quot;</td>', 
                  f'<td style="width:{img_width}px;vertical-align:top"><img " src="\\1"/></td>', 
                  output)
    display(HTML(html))


# -

# The Kypher-V example queries in this notebook assume the existence of a number of similarity
# graph caches in the `DB` directory, which are all defined here via shell variables:

DB="/kgtk-data/kypherv"
# %env DB={DB}
# %env MAIN={DB}/wikidata-20221102-dwd-v8-main.sqlite3.db
# %env COMPLEX={DB}/wikidata-20221102-dwd-v8-complex-embeddings.sqlite3.db
# %env TRANSE={DB}/wikidata-20221102-dwd-v8-transe-embeddings.sqlite3.db
# %env ABSTRACT={DB}/wikidata-20221102-dwd-v8-abstract-embeddings.sqlite3.db
# %env IMAGE={DB}/wikimedia-capcom-image-embeddings-v2.sqlite3.db

# If you copied the graph caches and their associated `.faiss.idx` ANNS index files
# to a different location, please adjust the paths and definitions accordingly.

# Throughout the notebook we use three different invocation styles for
# the `kgtk` command to better control the appearance of the generated output.
# We either use it via the `!kgtk ...` syntax directly, use the `kgtk(...)`
# function which produces an HTML rendering of a Pandas frame containing the
# result, or we use the `show_html` function for some additional control on
# how long texts and inline images are displayed.  All of these incantations
# should be straightforward to translate into a shell environment if needed.


# <A NAME="graph-caches"></A>
# ### Similarity graph caches
#
# The examples in this notebook rely on several standard and similarity
# graph caches based on `wikidata-20221102-dwd-v8`.  These graph caches are
# available in the `DB` directory of the `ckg06` server from where they can be
# copied or accessed directly in example queries.  It will generally not be
# possible to run the notebook directly from that server, so if you want to
# run and experiment with the notebook in a Jupyter environment, you have to
# # copy the graph caches to a different location where a notebook server can be run.
# In this case, make sure to also copy the associated ANNS index files that end in
# a `.faiss.idx` extension.

# This notebook does not show how the individual similarity caches were
# constructed.  To see how that can be done, please consult
# the [**Kypher-V Manual**](https://kgtk.readthedocs.io/en/latest/transform/query/#kypher-v)
# or look at the respective `*.db.build.txt` files in the `DB` directory.  For reference,
# we show just one incantation here on how the `COMPLEX` graph cache was built.  Other
# graph caches were built similarly with some modifications to adjust for differences in
# the embedding data used (for `COMPLEX` this takes about 2.5-3 hours to run on a laptop):

# ```
# $ export WD=.../datasets/wikidata-20221102-dwd-v8
#
# $ cat $WD/wikidatadwd.complEx.graph-embeddings.txt | sed -e 's/ /\t/' \
#       | kgtk --debug add-id --no-input-header=False --input-column-names node1 node2 \
#                    --implied-label emb \
#            / query --gc $DB/wikidata-20221102-dwd-v8-complex-embeddings.sqlite3.db \
#                    -i - --as complex \
#                    --idx vector:node2/nn/ram=25g/nlist=16k mode:valuegraph \
#                    --single-user --limit 5
# ```

# We use the following similarity graph caches which can be combined
# with a main graph cache using one or more `--auxiliary-cache` or `--ac`
# options to the `query` command.  The `COMPLEX` graph cache contains
# 59M 100-D ComplEx graph embeddings:

# !kgtk query --gc $COMPLEX --sc

# The `TRANSE` graph cache contains 59M 100-D TransE graph embeddings:

# !kgtk query --gc $TRANSE --sc

# The `ABSTRACT` graph cache contains the sentences and embedding vectors
# generated from the first sentences of Wikipedia short abstracts.  It
# contains about 6M 768-D Roberta base vectors:

# !kgtk query --gc $ABSTRACT --sc

# The `IMAGE` graph cache contains image embeddings published by the
# <a href="https://techblog.wikimedia.org/2021/09/09/the-wikipedia-image-caption-matching-challenge-and-a-huge-release-of-image-data-for-research/">
# Wikipedia image/caption matching challenge</a>.  The embeddings are 2048-D vectors
# taken from the second-to-last layer of a ResNet-50 neural network trained with
# Imagenet data.  We only use the 2.7M images associated with English Wikipedia
# pages.  The resulting vector graph cache is shown here:

# !kgtk query --gc $IMAGE --sc

# Finally, we also use a standard Wikidata graph cache for the claims and
# labels of `wikidata-20221102-dwd-v8`.  It is called `MAIN` below.


# <A NAME="vector-tables"></A>
# ### Vector tables are regular KGTK files
#
# Any KGTK representation that associates a node or edge ID with a vector
# will work.  An edge format we commonly use is a `node1` pointing to a vector
# literal in `node2` via an `emb` edge (but any label will do).  For example,
# here we show the first three embedding edges in `COMPLEX` (the `node2;_kgtk_vec_qcell`
# column is an auxiliary column automatically computed by ANNS indexing):

kgtk("""query --gc $COMPLEX -i complex --limit 3""")


# <A NAME="vector-computation"></A>
# ### Vector computation

# The simplest operation in Kypher-V is a similarity computation between two vectors
# which we perform here using the `ABSTRACT` graph cache:

kgtk(""" 
      query --gc $MAIN --ac $ABSTRACT
      -i abstract -i labels
      --match 'abstract: (x:Q868)-->(xv),
                         (y:Q913)-->(yv),
               labels:   (x)-->(xl), (y)-->(yl)'
      --return 'xl as xlabel, yl as ylabel, kvec_cos_sim(xv, yv) as sim'
     """)


# <A NAME="brute-force-search"></A>
# ### Brute-force similarity search

# A more interesting operation is *similarity search* where we look
# for the most similar matches for a given seed.  In the query below, we
# use a simple but expensive brute-force search over about 10,000 input
# vectors by computing similarities between `x` and each possible `y`,
# then sorting and returning the top-10.  This is still pretty fast
# given that the set of inputs is fairly small:

kgtk("""
      query --gc $MAIN --ac $ABSTRACT
      -i abstract -i labels -i claims
      --match 'abstract: (x:Q913)-->(xv), (y)-->(yv),
               claims:   (y)-[:P106]->(:Q4964182),
               labels:   (x)-->(xl), (y)-->(yl)'
      --return 'xl as xlabel, yl as ylabel, kvec_cos_sim(xv, yv) as sim'
      --order  'sim desc'
      --limit 10
     """)

# There are about 9M Q5's (humans) in Wikidata, 1.8M of which have short abstract vectors:

kgtk("""
      query --gc $MAIN --ac $ABSTRACT
      -i abstract -i claims
      --match 'abstract: (x)-->(),
               claims:   (x)-[:P31]->(:Q5)'
      --return 'count(distinct x)'
     """)


# If we used the same brute-force search from above on this much larger set,
# it would take about 5 min to run (which is why this command is disabled):

# !time DISABLED kgtk query --gc $MAIN \
#                  --ac $ABSTRACT \
#       -i abstract -i labels -i claims \
#       --match 'abstract: (x:Q913)-->(xv), (y)-->(yv), \
#                claims:   (y)-[:P31]->(:Q5), \
#                labels:   (x)-->(xl), (y)-->(yl)' \
#       --return 'xl as xlabel, yl as ylabel, kvec_cos_sim(xv, yv) as sim' \
#       --order  'sim desc' \
#       --limit 10

# ```
# xlabel	ylabel	sim
# 'Socrates'@en	'Socrates'@en	1.0000001192092896
# 'Socrates'@en	'Anytus'@en	0.9346579909324646
# 'Socrates'@en	'Heraclitus'@en	0.9344534277915955
# 'Socrates'@en	'Hippocrates'@en	0.9304061532020569
# 'Socrates'@en	'Cleisthenes'@en	0.9292828440666199
# 'Socrates'@en	'Aristides'@en	0.9283562898635864
# 'Socrates'@en	'Yannis Xirotiris'@en	0.926308274269104
# 'Socrates'@en	'Sotiris Trivizas'@en	0.9255445003509521
# 'Socrates'@en	'Aris Maragkopoulos'@en	0.9234243035316467
# 'Socrates'@en	'Valerios Stais'@en	0.919943630695343
# 93.859u 38.640s 4:49.84 45.7%	0+0k 18782808+8io 0pf+0w
# ```

# <A NAME="indexed-search"></A>
# ### Indexed similarity search

# For much faster search, we use an ANNS index constructed when the vector data
# was imported which now runs in less than a second compared to 5 minutes before.
# Results here are slightly different from above, since it does not restrict on
# occupation = philosopher (we will address that later):

kgtk("""
      query --gc $MAIN --ac $ABSTRACT
      -i abstract -i labels -i claims
      --match 'abstract: (x:Q913)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 5, nprobe: 4}]->(y),
               labels:   (x)-->(xl), (y)-->(yl)'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
      --limit 10
     """)


# <A NAME="similarity-join"></A>
# ### Full similarity join
#
# Below we query for three philosophers' top-k similar neighbors that are also humans and have
# occupation (`P106`) philosopher.  Dynamic scaling ensures that `k` gets increased dynamically
# up to `maxk` until we've found enough qualifying results for each:

kgtk("""
      query --gc $MAIN --ac $ABSTRACT
      -i abstract -i labels -i claims
      --match 'abstract: (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 5, maxk: 1024, nprobe: 4}]->(y),
               claims:   (y)-[:P106]->(:Q4964182),
                         (y)-[:P31]->(:Q5),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q859", "Q868", "Q913"] and x != y'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)


# For comparison, here is a run without dynamic scaling which returns much fewer results, since
# only a small number of the top-5 similar results for each input also satisfy the post conditions:

kgtk("""
      query --gc $MAIN --ac $ABSTRACT
      -i abstract -i labels -i claims
      --match 'abstract: (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 5, nprobe: 4}]->(y),
               claims:   (y)-[:P106]->(:Q4964182),
                         (y)-[:P31]->(:Q5),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q859", "Q868", "Q913"] and x != y'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)


# <A NAME="applications"></A>
# ## Example applications

# ### Image search

# In the examples below, we use image similarity to link QNodes in Wikidata.  We
# use the precomputed `IMAGE` graph cache (see above) which contains embeddings
# for about 2.7M images linked to their respective Wikipedia pages and Wikidata
# QNodes.  

# We start with a QNode (such a the one for Barack Obama below), find one or more
# images associated with that QNode, look up their image embeddings and then find
# other similar images and their associated QNodes.

# We do not compute any image embeddings on the fly here, we simply link nodes based
# on similarity of images they are associated with.  Note that this will often not
# preserve the type of the source node as can be seen in the result for Barack Obama.
# To enforce such type or other restrictions additional clauses can be added.
# Since there are multiple images associated with Barack Obama, we use a `not exists`
# clause to only look at the first one to make the results less cluttered:
#
# Barack Obama:

# +
# out = !kgtk query --gc $IMAGE --ac $MAIN \
#       -i wiki_image -i labels \
#       --match 'image:  (ximg)-[rx {qnode: $SEED}]->(xiv), \
#                        (xiv)-[r:kvec_topk_cos_sim {k: 10, nprobe: 8}]->(yimg), \
#                        (yimg)-[ry {qnode: y}]->(), \
#                labels: (y)-->(ylabel)' \
#       --where 'not exists {image: (ximg2)-[{qnode: $SEED}]->() WHERE rowid(ximg2) < rowid(ximg) }' \
#       --return 'y as qnode, ylabel as label, printf("%.5g", r.similarity) as sim, yimg as image' \
#       --para  SEED=Q76 \
#     / html

show_html(img_width=200)
# -

# To get more type appropriate matches, we can add a restriction to only return matches of
# type human (`Q5`):

# +
# out = !kgtk query --gc $IMAGE --ac $MAIN \
#       -i wiki_image -i labels -i claims \
#       --match 'image:  (ximg)-[rx {qnode: $SEED}]->(xiv), \
#                        (xiv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(yimg), \
#                        (yimg)-[ry {qnode: y}]->(), \
#                claims: (y)-[:P31]->(:Q5), \
#                labels: (y)-->(ylabel)' \
#       --where 'not exists {image: (ximg2)-[{qnode: $SEED}]->() WHERE rowid(ximg2) < rowid(ximg) }' \
#       --return 'y as qnode, ylabel as label, printf("%.5g", r.similarity) as sim, yimg as image' \
#       --para  SEED=Q76 \
#     / html

show_html(img_width=200)
# -

# Charles Dadant: again, note that some of the results are not of type human but are
# just linked to a similar image:

# +
# out = !kgtk query --gc $IMAGE --ac $MAIN \
#       -i wiki_image -i labels \
#       --match 'image: (ximg)-[rx {qnode: $SEED}]->(xiv), \
#                       (xiv)-[r:kvec_topk_cos_sim {k: 10, nprobe: 8}]->(yimg), \
#                       (yimg)-[ry {qnode: y}]->(), \
#                labels: (y)-->(ylabel)' \
#       --where 'not exists {image: (ximg2)-[{qnode: $SEED}]->() WHERE rowid(ximg2) < rowid(ximg) }' \
#       --return 'y as qnode, ylabel as label, printf("%.5g", r.similarity) as sim, yimg as image' \
#       --para  SEED=Q582964 \
#       --limit 20 \
#     / html

show_html(img_width=100)
# -

# Beaumaris Castle in Wales:

# +
# out = !kgtk query --gc $IMAGE --ac $MAIN \
#       -i wiki_image -i labels \
#       --match 'image: (ximg)-[rx {qnode: $SEED}]->(xiv), \
#                       (xiv)-[r:kvec_topk_cos_sim {k: 20, nprobe: 8}]->(yimg), \
#                       (yimg)-[ry {qnode: y}]->(), \
#                labels: (y)-->(ylabel)' \
#       --where 'not exists {image: (ximg2)-[{qnode: $SEED}]->() WHERE rowid(ximg2) < rowid(ximg) }' \
#       --return 'y as qnode, ylabel as label, printf("%.5g", r.similarity) as sim, yimg as image' \
#       --para  SEED=Q756815  \
#     / html

show_html()
# -


# <A NAME="image-similarity-join"></A>

# Castles similar to Beaumaris Castle but that are located in Austria (with
# country (`P17`) equal to `Q40`).  We use a full vector join to get relevant
# results further down the similarity list.  Note that even with `maxk=1024` we only
# get a few results, and that the similarities are significantly lower than in the
# previous example:

# +
# out = !kgtk query --gc $IMAGE --ac $MAIN \
#       -i wiki_image -i labels -i claims \
#       --match 'image: (ximg)-[rx {qnode: $SEED}]->(xiv), \
#                       (xiv)-[r:kvec_topk_cos_sim {k: 20, nprobe: 4, maxk: 1024}]->(yimg), \
#                       (yimg)-[ry {qnode: y}]->(), \
#                labels: (y)-->(ylabel), \
#                claims: (y)-[:P17]->(c:Q40)' \
#       --where 'not exists {image: (ximg2)-[{qnode: $SEED}]->() WHERE rowid(ximg2) < rowid(ximg) }' \
#       --return 'y as qnode, ylabel as label, printf("%.5g", r.similarity) as sim, yimg as image' \
#       --para  SEED=Q756815  \
#       --limit 20 \
#     / html

show_html()
# -


# <A NAME="text-embedding-queries"></A>
# ## Text embedding queries:

# In the following example we dynamically compute an embedding vector
# for a text query and then use the similarity machinery to query for
# matching QNodes.  The basic story here is the following:

# - formulate a simple textual query such as 'Ancient Greek philosopher'
# - create a KGTK input file for it/them and run them through the 'text-embedding' command
# - query WD by finding top-k matches based on short abstract text embedding vectors
# - then filter with additional restrictions to get more relevant results.

# !echo '\
# q1	Ancient Greek philosopher\n\
# q2	castle in Austria\n\
# q3	award-winning actor and comedian' | \
# sed -e 's/^ *//' | \
# kgtk cat --no-input-header --input-column-names node1 node2 --implied-label sentence \
#    / add-id \
#    / text-embedding -i - --model roberta-base-nli-mean-tokens \
#           --output-data-format kgtk --output-property emb -o - \
#    / query -i - --idx vector:node2 --as text_emb_queries --match '(x)' --return x

# The above created 768-D text embedding vector for three short queries
# using the same text embedding type as used in our `ABSTRACT` embeddings.
# Now we find Wikidata QNodes whose short-abstract embedding vector is most similar
# to the queries, and that satisfy any additional conditions we might have.
# Note that the queries in this example are much shorter than the first sentences
# of our Wikipedia abstracts, thus the similarity matching is not very good, but
# we can compensate for some of that by adding additional restrictions:

# Matches for "Ancient Greek philosopher" that have occupation (`P106`) philosopher:

# +
# out = !kgtk query --ac $MAIN --ac $ABSTRACT \
#       -i text_emb_queries -i abstract -i labels -i claims -i sentence \
#       --match  'queries:  (x:q1)-->(xv), \
#                 abstract: (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 4}]->(y), \
#                 claims:   (y)-[:P106]->(:Q4964182), \
#                 labels:   (y)-->(yl), \
#                 sentence: (y)-->(ys)' \
#       --return 'y as y, yl as ylabel, r.similarity as sim, kgtk_lqstring_text(ys) as ysent' \
#     / html

show_html()
# -

# Matches for "castle in Austria" that have country (`P17`) Austria:

# +
# out = !kgtk query --ac $MAIN --ac $ABSTRACT \
#       -i text_emb_queries -i abstract -i labels -i claims -i sentence \
#       --match  'queries:  (x:q2)-->(xv), \
#                 abstract: (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y), \
#                 claims:   (y)-[:P17]->(:Q40), \
#                 labels:   (y)-->(yl), \
#                 sentence: (y)-->(ys)' \
#       --return 'y as y, yl as ylabel, r.similarity as sim, kgtk_lqstring_text(ys) as ysent' \
#     / html

show_html()
# -

# Matches for "award-winning actor and comedian" that are of type human
# and have country of citizenship (`P27`) UK:

# +
# out = !kgtk query --ac $MAIN --ac $ABSTRACT \
#       -i text_emb_queries -i abstract -i labels -i claims -i sentence \
#       --match  'queries:  (x:q3)-->(xv), \
#                 abstract: (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y), \
#                 claims:   (y)-[:P31]->(:Q5), \
#                           (y)-[:P27]->(:Q145), \
#                 labels:   (y)-->(yl), \
#                 sentence: (y)-->(ys)' \
#       --return 'y as y, yl as ylabel, r.similarity as sim, kgtk_lqstring_text(ys) as ysent' \
#     / html

show_html()
# -


# <A NAME="comparing-embeddings"></A>
# ## Comparing different types of embeddings

# Below we run a number of similarity queries for each of our various types of
# embeddings to see how they behave relative to each other.  Note how they
# behave quite differently, reasonable for some use cases but not so much for others:

# ### Philosophers:

kgtk("""
      query --gc $MAIN --ac $COMPLEX
      -i complex -i labels
      --match 'complex:  (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q859", "Q868", "Q913"]'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)

kgtk("""
      query --gc $MAIN --ac $TRANSE
      -i transe -i labels
      --match 'transe:   (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q859", "Q868", "Q913"]'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)

# +
# out = !kgtk query --gc $MAIN --ac $ABSTRACT \
#       -i abstract -i labels -i sentence \
#       --match 'abstract: (x)-->(xv), \
#                          (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y), \
#                labels:   (x)-->(xl), (y)-->(yl), \
#                sent:     (y)-->(ys)' \
#       --where 'x in ["Q859", "Q868", "Q913"]' \
#       --return 'xl as xlabel, yl as ylabel, r.similarity as sim, kgtk_lqstring_text(ys) as ysent' \
#     / html

show_html()
# -


# ### Countries:

kgtk("""
      query --gc $MAIN --ac $COMPLEX
      -i complex -i labels
      --match 'complex:  (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q40", "Q41", "Q30"]'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)

kgtk("""
      query --gc $MAIN --ac $TRANSE
      -i transe -i labels
      --match 'transe:   (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q40", "Q41", "Q30"]'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)

# +
# out = !kgtk query --gc $MAIN --ac $ABSTRACT \
#       -i abstract -i labels -i sentence \
#       --match 'abstract: (x)-->(xv), \
#                          (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y), \
#                labels:   (x)-->(xl), (y)-->(yl), \
#                sent:     (y)-->(ys)' \
#       --where 'x in ["Q40", "Q41", "Q30"]' \
#       --return 'xl as xlabel, yl as ylabel, r.similarity as sim, kgtk_lqstring_text(ys) as ysent' \
#     / html

show_html()
# -


# ### Types of animals:

kgtk("""
      query --gc $MAIN --ac $COMPLEX
      -i complex -i labels
      --match 'complex:  (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q144", "Q146", "Q726"]'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)

kgtk("""
      query --gc $MAIN --ac $TRANSE
      -i transe -i labels
      --match 'transe:   (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q144", "Q146", "Q726"]'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)

# +
# out = !kgtk query --gc $MAIN --ac $ABSTRACT \
#       -i abstract -i labels -i sentence \
#       --match 'abstract: (x)-->(xv), \
#                          (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y), \
#                labels:   (x)-->(xl), (y)-->(yl), \
#                sent:     (y)-->(ys)' \
#       --where 'x in ["Q144", "Q146", "Q726"]' \
#       --return 'xl as xlabel, yl as ylabel, r.similarity as sim, kgtk_lqstring_text(ys) as ysent' \
#     / html

show_html()
# -


# ### Handball:

kgtk("""
      query --gc $MAIN --ac $COMPLEX
      -i complex -i labels
      --match 'complex:  (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q8418"]'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)

kgtk("""
      query --gc $MAIN --ac $TRANSE
      -i transe -i labels
      --match 'transe:   (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q8418"]'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)

# +
# out = !kgtk query --gc $MAIN --ac $ABSTRACT \
#       -i abstract -i labels -i sentence \
#       --match 'abstract: (x)-->(xv), \
#                          (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y), \
#                labels:   (x)-->(xl), (y)-->(yl), \
#                sent:     (y)-->(ys)' \
#       --where 'x in ["Q8418"]' \
#       --return 'xl as xlabel, yl as ylabel, r.similarity as sim, kgtk_lqstring_text(ys) as ysent' \
#     / html

show_html()
# -


# ### Journalist:

kgtk("""
      query --gc $MAIN --ac $COMPLEX
      -i complex -i labels
      --match 'complex:  (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q1930187"]'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)

kgtk("""
      query --gc $MAIN --ac $TRANSE
      -i transe -i labels
      --match 'transe:   (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q1930187"]'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)

# +
# out = !kgtk query --gc $MAIN --ac $ABSTRACT \
#       -i abstract -i labels -i sentence \
#       --match 'abstract: (x)-->(xv), \
#                          (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y), \
#                labels:   (x)-->(xl), (y)-->(yl), \
#                sent:     (y)-->(ys)' \
#       --where 'x in ["Q1930187"]' \
#       --return 'xl as xlabel, yl as ylabel, r.similarity as sim, kgtk_lqstring_text(ys) as ysent' \
#     / html

show_html()
# -


# ### Head of state:

kgtk("""
      query --gc $MAIN --ac $COMPLEX
      -i complex -i labels
      --match 'complex:  (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q48352"]'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)

kgtk("""
      query --gc $MAIN --ac $TRANSE
      -i transe -i labels
      --match 'transe:   (x)-->(xv),
                         (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y),
               labels:   (x)-->(xl), (y)-->(yl)'
      --where 'x in ["Q48352"]'
      --return 'xl as xlabel, yl as ylabel, r.similarity as sim'
     """)

# +
# out = !kgtk query --gc $MAIN --ac $ABSTRACT \
#       -i abstract -i labels -i sentence \
#       --match 'abstract: (x)-->(xv), \
#                          (xv)-[r:kvec_topk_cos_sim {k: 10, maxk: 1024, nprobe: 8}]->(y), \
#                labels:   (x)-->(xl), (y)-->(yl), \
#                sent:     (y)-->(ys)' \
#       --where 'x in ["Q48352"]' \
#       --return 'xl as xlabel, yl as ylabel, r.similarity as sim, kgtk_lqstring_text(ys) as ysent' \
#     / html

show_html()
