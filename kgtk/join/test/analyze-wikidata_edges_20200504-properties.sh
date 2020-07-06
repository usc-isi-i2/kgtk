#! /bin/bash

PROPERTY=P580
WORKDIR=task-20200624
WIKIDATADIR=../../cache/datasets/wikidata-20200504
# WIKIDATAGZIP=.gz
WIKIDATAGZIP=

# VERBOSE=
VERBOSE=--verbose

# KGTK=echo
# KGTK="kgtk"
KGTK="python3 -m kgtk"

# Extract the qualifiers with ${PROPERTY} in the label column.
${KGTK} filter ${VERBOSE} \
     ${WIKIDATADIR}/wikidata_qualifiers_20200504.tsv${WIKIDATAGZIP} \
     -o ${WORKDIR}/wikidata_qualifiers_20200504-${PROPERTY}.tsv
     -p "; ${PROPERTY} ;" \

# Extract the edges with ID column values that match node1 column
# values from the extracted qualifiers.
${KGTK} ifexists ${VERBOSE} \
     ${WIKIDATADIR}/wikidata_edges_20200504.tsv${WIKIDATAGZIP} \
     -o ${WORKDIR}/wikidata_edges_20200504-${PROPERTY}.tsv
     --filter-on ${WORKDIR}/wikidata_qualifiers_20200504-${PROPERTY}.tsv \
     --input-keys id \
     --filter-keys node1 \

# Count the properties in the property-qualified edge file:
${KGTK} unique ${VERBOSE} \
     ${WORKDIR}/wikidata_edges_20200504-${PROPERTY}.tsv \
     -o ${WORKDIR}/wikidata_edges_20200504-${PROPERTY}-property-counts.tsv
     --column label \
     --label ${PROPERTY}-count \

# Merge the total count with lift.
${KGTK} lift ${VERBOSE} \
     ${WORKDIR}/wikidata_edges_20200504-${PROPERTY}-property-counts.tsv \
     --label-file ${WORKDIR}/wikidata_edges_20200504-property-counts.tsv \
     --output-file ${WORKDIR}/wikidata_edges_20200504-${PROPERTY}-property-counts-with-totals.tsv \
     --columns-to-lift node1 \
     --label-value total-count \
     --lift-suffix ';total' \

# Calculate the percentages:
${KGTK} calc ${VERBOSE} \
     -i ${WORKDIR}/wikidata_edges_20200504-${PROPERTY}-property-counts-with-totals.tsv \
     -o ${WORKDIR}/wikidata_edges_20200504-${PROPERTY}-property-counts-with-percents.tsv \
     -c node2 'node1;total' \
     --do percentage \
     --into percent \

# Lift the property labels:
${KGTK} lift ${VERBOSE} \
      ${WORKDIR}/wikidata_edges_20200504-${PROPERTY}-property-counts-with-percents.tsv \
     --label-file ${WIKIDATADIR}/wikidata_labels_only.tsv${WIKIDATAGZIP} \
     --output-file ${WORKDIR}/wikidata_edges_20200504-${PROPERTY}-property-counts-with-labels.tsv \
     --columns-to-lift node1 \
     --prefilter-labels \
