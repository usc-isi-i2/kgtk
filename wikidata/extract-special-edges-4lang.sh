#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Extract the property datatypes.
echo -e "\nExtract the property datatypes from the edge file."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_EDGES}-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL_EDGES}-property-datatypes-sorted.tsv \
     --pattern '; datatype ;' \
    |& tee ${LOGDIR}/${WIKIDATA_ALL_EDGES}-property-datatypes-sorted.log

echo -e "\nCount the property datatypes."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_EDGES}-property-datatypes-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL_EDGES}-property-datatype-counts.tsv \
     --column node2 \
    |& tee ${LOGDIR}/${WIKIDATA_ALL_EDGES}-property-datatype-counts.log

echo -e "\nExtract the properties with external IDs."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_EDGES}-property-datatypes-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL_EDGES}-external-id-properties-sorted.tsv \
     --pattern ';; external-id' \
     |& tee ${LOGDIR}/${WIKIDATA_ALL_EDGES}-external-id-properties-sorted.log


# ==============================================================================
# Extract the sitelinks.
echo -e "\nExtract the sitelinks."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_EDGES}-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-sitelinks-sorted.tsv \
     --reject-file ${DATADIR}/${WIKIDATA_ALL_EDGES}-without-sitelinks-sorted.tsv \
     --pattern '; wikipedia_sitelink ;' \
    |& tee ${LOGDIR}/${WIKIDATA_ALL}-sitelinks-sorted.log

echo -e "\nExtract the additional sitelinks."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_EDGES}-without-sitelinks-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-addl-sitelinks-sorted.tsv \
     --reject-file ${DATADIR}/${WIKIDATA_ALL_EDGES}-without-any-sitelinks-sorted.tsv \
     --pattern '; addl_wikipedia_sitelink ;' \
    |& tee ${LOGDIR}/${WIKIDATA_ALL}-addl-sitelinks-sorted.log


# ==============================================================================
# Normalize the node files into edge files.
#
echo -e "\nNormalize the node file in all languages"
kgtk ${KGTK_FLAGS} \
     normalize-nodes ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_NODES}-all-lang-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-all-lang-sorted.tsv \
    |& tee ${LOGDIR}/${WIKIDATA_ALL}-labels-etc-all-lang-sorted.log

echo -e "\nNormalize the node file in English only"
kgtk ${KGTK_FLAGS} \
     normalize-nodes ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_NODES}-en-only-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-en-only-sorted.tsv \
    |& tee ${LOGDIR}/${WIKIDATA_ALL}-labels-etc-en-only-sorted.log

echo -e "\nNormalize the node file in English, Spanish, Russian, and Ukranian."
kgtk ${KGTK_FLAGS} \
     normalize-nodes ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_NODES}-en-es-ru-uk-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-en-es-ru-uk-sorted.tsv \
    |& tee ${LOGDIR}/${WIKIDATA_ALL}-labels-etc-en-es-ru-uk-sorted.log

# ==============================================================================
# Extract the alias, datatype, description, and label edges for all languages.
echo -e "\nExtract the alias edges for all languages."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-all-lang-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-aliases-all-lang-sorted.tsv \
     --pattern '; alias ;' \
    |& tee ${WIKIDATA_ALL}-aliases-all-lang-sorted.log

echo -e "\nExtract the datatype edges for all languages."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-all-lang-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-datatypes-all-lang-sorted.tsv \
     --pattern '; datatype ;' \
    |& tee ${WIKIDATA_ALL}-datatypes-all-lang-sorted.log

echo -e "\nExtract the description edges for all languages."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-all-lang-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-descriptions-all-lang-sorted.tsv \
     --pattern '; description ;' \
    |& tee ${WIKIDATA_ALL}-descriptions-all-lang-sorted.log

echo -e "\nExtract the label edges for all languages."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-all-lang-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-labels-only-all-lang-sorted.tsv \
     --pattern '; label ;' \
    |& tee ${WIKIDATA_ALL}-labels-only-all-lang-sorted.log

# ==============================================================================
# Extract the alias, datatype, description, and label edges for English only.
echo -e "\nExtract the alias edges for English only."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-en-only-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-aliases-en-only-sorted.tsv \
     --pattern '; alias ;' \
    |& tee ${WIKIDATA_ALL}-aliases-en-only-sorted.log

echo -e "\nExtract the datatype edges for English only."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-en-only-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-datatypes-en-only-sorted.tsv \
     --pattern '; datatype ;' \
    |& tee ${WIKIDATA_ALL}-datatypes-en-only-sorted.log

echo -e "\nExtract the description edges for English only."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-en-only-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-descriptions-en-only-sorted.tsv \
     --pattern '; description ;' \
    |& tee ${WIKIDATA_ALL}-descriptions-en-only-sorted.log

echo -e "\nExtract the label edges for English only."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-en-only-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-labels-only-en-only-sorted.tsv \
     --pattern '; label ;' \
    |& tee ${WIKIDATA_ALL}-labels-only-en-only-sorted.log

# ==============================================================================
# Extract the alias, datatype, description, and label edges for English, Spanish, Russian, and Ukranian.
echo -e "\nExtract the alias edges for English, Spanish, Russian, and Ukranian."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-en-sp-ru-uk-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-aliases-en-sp-ru-uk-sorted.tsv \
     --pattern '; alias ;' \
    |& tee ${WIKIDATA_ALL}-aliases-en-sp-ru-uk-sorted.log

echo -e "\nExtract the datatype edges for English, Spanish, Russian, and Ukranian."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-en-sp-ru-uk-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-datatypes-en-sp-ru-uk-sorted.tsv \
     --pattern '; datatype ;' \
    |& tee ${WIKIDATA_ALL}-datatypes-en-sp-ru-uk-sorted.log

echo -e "\nExtract the description edges for English, Spanish, Russian, and Ukranian."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-en-sp-ru-uk-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-descriptions-en-sp-ru-uk-sorted.tsv \
     --pattern '; description ;' \
    |& tee ${WIKIDATA_ALL}-descriptions-en-sp-ru-uk-sorted.log

echo -e "\nExtract the label edges for English, Spanish, Russian, and Ukranian."
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-labels-etc-en-sp-ru-uk-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-labels-only-en-sp-ru-uk-sorted.tsv \
     --pattern '; label ;' \
    |& tee ${WIKIDATA_ALL}-labels-only-en-sp-ru-uk-sorted.log

# ==============================================================================
echo -e "\nCount the properties in ${DATADIR}/${WIKIDATA_ALL_EDGES}-sorted.tsv."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL_EDGES}-sorted.tsv \
     --output-file ${DATADIR}${WIKIDATA_ALL}-property-counts.tsv \
     --column label \
     --label total-count \
     |& tee logs/${WIKIDATA_ALL}-property-counts.log

echo -e "\nLift the English property labels:"
kgtk ${KGTK_FLAGS} \
     lift ${VERBOSE} \
     --input-file ${DATADIR}/${WIKIDATA_ALL}-property-counts.tsv \
     --label-file ${DATADIR}/${WIKIDATA_ALL}-labels-only-en-only-sorted.tsv \
     --output-file ${DATADIR}/${WIKIDATA_ALL}-property-counts-with-labels.tsv \
     --columns-to-lift node1 \
     --prefilter-labels \
     |& tee logs/${WIKIDATA_ALL}-property-counts-with-labels.log

# ==============================================================================
echo -e "\nCompress the data product files."
time gzip --keep --force --verbose \
     ${DATADIR}/${WIKIDATA_ALL_EDGES}-property-datatypes-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL_EDGES}-property-datatype-counts.tsv \
     ${DATADIR}/${WIKIDATA_ALL_EDGES}-external-id-properties-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-sitelinks-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-addl-sitelinks-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL_EDGES}-without-any-sitelinks-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-labels-etc-all-lang-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-labels-etc-en-only-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-labels-etc-en-es-ru-uk-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-aliases-all-lang-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-datatypes-all-lang-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-descriptions-all-lang-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-labels-only-all-lang-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-aliases-en-only-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-datatypes-en-only-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-descriptions-en-only-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-labels-only-en-only-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-aliases-en-sp-ru-uk-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-datatypes-en-sp-ru-uk-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-descriptions-en-sp-ru-uk-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-labels-only-en-sp-ru-uk-sorted.tsv \
     ${DATADIR}/${WIKIDATA_ALL}-property-counts-with-labels.tsv \
    |& tee ${LOGDIR}/extract-special-edges-compress.log

# ==============================================================================
echo -e "\nDeliver the compressed data products to the KGTK Google Drive."
time rsync --archive \
     *.tsv.gz \
     ${PRODUCTDIR}/ \
    |& tee ${LOGDIR}/extract-special-edges-deliver.log

     
     
