#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
echo -e "\nCount the properties in ${DATADIR}/claims.properties.tsv."
kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} \
     --input-file ${DATADIR}/claims.properties.${SORTED_KGTK} \
     --output-file ${DATADIR}/claims.properties.counts.${SORTED_KGTK} \
     --column label \
     --label total-count \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/claims.properties.counts.log


# ==============================================================================
echo -e "\nLift the property labels:"
#
# CMR: This step takes 10 minutes on my home workstation because
# ${DATADIR}/part.label.en.${SORTED_KGTK} is fairly large (6.6G
# as of 05-Oct-2020).
kgtk ${KGTK_FLAGS} \
     lift ${VERBOSE} \
     --input-file ${DATADIR}/claims.properties.counts.${SORTED_KGTK} \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/claims.properties.counts-with-labels.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --prefilter-labels \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/claims.properties.counts-with-labels.log

