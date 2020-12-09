#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
# Split out claim records with missing values.
echo -e "\nSplit somevalue and novalue from ${DATADIR}/rawclaims.tsv"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} --use-mgzip ${USE_MGZIP} \
     --input-file ${TEMPDIR}/claims.raw.${UNSORTED_KGTK} \
     --first-match-only \
     --pattern ";; novalue,somevalue"  -o ${TEMPDIR}/claims.missingValues.${UNSORTED_KGTK} \
     --reject-file ${TEMPDIR}/claims.${UNSORTED_KGTK} \
    |& tee ${LOGDIR}/split-claims-missing-values.log

# ==============================================================================
# Split out qualifier records with missing values.
echo -e "\nSplit somevalue and novalue from ${DATADIR}/rawqualifiers.tsv"
kgtk ${KGTK_FLAGS} \
     filter ${VERBOSE} --use-mgzip ${USE_MGZIP} \
     --input-file ${TEMPDIR}/qualifiers.raw.${UNSORTED_KGTK} \
     --first-match-only \
     --pattern ";; novalue,somevalue"  -o ${TEMPDIR}/qualifiers.missingValues.${UNSORTED_KGTK} \
     --reject-file ${TEMPDIR}/qualifiers.${UNSORTED_KGTK} \
    |& tee ${LOGDIR}/split-qualifiers-missing-values.log
