#! /bin/bash

# This script expects to be executed with the current working directory:
#
# kgtk/datasets/time-machine-20101201
source common.sh

# ==============================================================================
echo -e "\nSort the claims file by id: ${DATADIR}/claims.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     sort2 ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --columns id \
     --input-file ${DATADIR}/claims.${SORTED_KGTK} \
     --gzip-command ${GZIP_CMD} \
     --extra "${SORT_EXTRAS}" \
     --output-file ${DATADIR}/claims.sorted-by-id.${SORTED_KGTK}

# ==============================================================================
echo -e "\nSort the qualifiers file by node1: ${DATADIR}/qualifiers.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     sort2 ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --columns node1 \
     --input-file ${DATADIR}/qualifiers.${SORTED_KGTK} \
     --gzip-command ${GZIP_CMD} \
     --extra "${SORT_EXTRAS}" \
     --output-file ${DATADIR}/qualifiers.sorted-by-node1.${SORTED_KGTK}

# ==============================================================================
echo -e "\nMerge the claims and the qualifiers, dropping unmatched qualifiers."
kgtk ${KGTK_FLAGS} \
     ifexists ${VERBOSE} --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/claims.sorted-by-id.${SORTED_KGTK} \
     --input-keys id \
     --filter-on ${DATADIR}/qualifiers.sorted-by-node1.${SORTED_KGTK} \
     --filter-keys node1 \
     --left-join --join-output \
     --output-file ${DATADIR}/claims-and-qualifiers.${SORTED_KGTK} \


