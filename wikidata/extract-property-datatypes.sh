#! /bin/bash

source common.sh

PART=all

# ==============================================================================
echo -e "\nExtract the node2;wikidatatype for each property in the label column of ${DATADIR}/${PART}.${SORTED_KGTK}."
# In the second sort, we do an alpha sort on the count field, which is
# problematic.  We'd also like to sort the count descending (reverse), but
# sort the other fields ascending.
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/${PART}.${SORTED_KGTK} \
     -p '; ^P[^-]*$ ;' \
     / calc ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --do copy \
     --columns  label 'node2;wikidatatype' \
     --into     node1  node2 \
     / calc ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --do set --value datatype --into label \
     / remove-columns ${VERBOSE} --use-mgzip=$USE_MGZIP --split-on-spaces \
     --all-except --columns node1 label node2 \
     / sort2 ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --gzip-command ${GZIP_CMD} \
     --extra "${SORT_EXTRAS}" \
     / compact ${VERBOSE} --use-mgzip=$USE_MGZIP --presorted \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     / tee $VERBOSE --use-mgzip=$USE_MGZIP \
     --into-file ${DATADIR}/${PART}.properties.datatypes.${SORTED_KGTK} \
     / unique ${VERBOSE} --use-mgzip=$USE_MGZIP --presorted \
     --column node1 \
     --label datatype-count \
     / lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     / sort2 ${VERBOSE} --use-mgzip=$USE_MGZIP --pure-python \
     --columns node2 node1 label \
     --output-file ${DATADIR}/${PART}.properties.datatypes.counts.${SORTED_KGTK}
