#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Split out claim records with so-called missing values.  The claims with the
# node2 value "novalue" will be put into "claims.novalue.tsv".  The claims
# with the node2 value "somevalue" will be put into "claims.somevalue.tsv".
echo -e "\nSplit somevalue and novalue from ${DATADIR}/claims.raw.tsv"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} --use-mgzip ${USE_MGZIP} \
     --input-file ${TEMPDIR}/claims.raw.${UNSORTED_KGTK} \
     --first-match-only \
     --pattern ";; novalue"  -o ${TEMPDIR}/claims.novalue.${UNSORTED_KGTK} \
     --pattern ";; somevalue"  -o ${TEMPDIR}/claims.somevalue.${UNSORTED_KGTK} \
     --reject-file ${TEMPDIR}/claims.${UNSORTED_KGTK} \
    | tee ${LOGDIR}/split-claims-missing-values.log

# ==============================================================================
# Split out qualifier records with so-called missing values.  The qualifiers with the
# node2 value "novalue" will be put into "qualifiers.novalue.tsv".  The qualifiers
# with the node2 value "somevalue" will be put into "qualifiers.somevalue.tsv".
#
# Split out qualifier records that are children of claim records with
# so-called missing values ("novalue" and "somevalue") (assumes that the claim
# records with missing values can be kept in memory).
#
# Split out qualifier records that are children of claim records with bad
# values (values that are invalid or which cannot be parsed in Python with
# standard libraries) (see import-split-wikidata-gzipped-clean.sh) (assumes
# that the claim records with bad values can be kept in memory).
echo -e "\nSplit somevalue and novalue from ${DATADIR}/qualifiers.raw.tsv"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} --use-mgzip ${USE_MGZIP} \
     --input-file ${TEMPDIR}/qualifiers.raw.${UNSORTED_KGTK} \
     --first-match-only \
     --pattern ";; novalue"  -o ${TEMPDIR}/qualifiers.novalue.${UNSORTED_KGTK} \
     --pattern ";; somevalue"  -o ${TEMPDIR}/qualifiers.somevalue.${UNSORTED_KGTK} \
     --reject-file - \
     / ifexists ${VERBOSE} \
     --input-keys node1 \
     --filter-file ${TEMPDIR}/claims.novalue.${UNSORTED_KGTK} \
     --filter-keys id \
     --output-file ${TEMPDIR}/qualifiers.novalueClaims.${UNSORTED_KGTK} \
     --reject-file - \
     / ifexists ${VERBOSE} \
     --input-keys node1 \
     --filter-file ${TEMPDIR}/claims.somevalue.${UNSORTED_KGTK} \
     --filter-keys id \
     --output-file ${TEMPDIR}/qualifiers.somevalueClaims.${UNSORTED_KGTK} \
     --reject-file - \
     / ifexists ${VERBOSE} \
     --input-keys node1 \
     --filter-file ${TEMPDIR}/claims.badvalue.${UNSORTED_KGTK} \
     --filter-keys id \
     --output-file ${TEMPDIR}/qualifiers.badvalueClaims.${UNSORTED_KGTK} \
     --reject-file ${TEMPDIR}/qualifiers.${UNSORTED_KGTK} \
    | tee ${LOGDIR}/split-qualifiers-missing-values.log
