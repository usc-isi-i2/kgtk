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
     --output-file ${DATADIR}/${PART}.properties.${SORTED_KGTK}

kgtk ${KGTK_FLAGS} \
     calc ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --input-file ${DATADIR}/${PART}.properties.${SORTED_KGTK} \
     --do copy \
     --columns  label 'node2;wikidatatype' \
     --into     node1  node2 \
     / calc ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --do set --value datatype --into label \
     / remove-columns ${VERBOSE} --use-mgzip=$USE_MGZIP --split-on-spaces \
     --all-except --columns node1 label node2 \
     --output-file ${DATADIR}/${PART}.properties.datatypes.unsorted.${SORTED_KGTK}
     
kgtk ${KGTK_FLAGS} \
     sort2 ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --input-file ${DATADIR}/${PART}.properties.datatypes.unsorted.${SORTED_KGTK} \
     --gzip-command ${GZIP_CMD} \
     --extra "${SORT_EXTRAS}" \
     --output-file ${DATADIR}/${PART}.properties.datatypes.sorted.${SORTED_KGTK}

kgtk ${KGTK_FLAGS} \
     compact ${VERBOSE} --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/${PART}.properties.datatypes.sorted.${SORTED_KGTK} \
     --output-file ${DATADIR}/${PART}.properties.datatypes.compacted.${SORTED_KGTK}

kgtk ${KGTK_FLAGS} \
     lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file ${DATADIR}/${PART}.properties.datatypes.compacted.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${DATADIR}/${PART}.properties.datatypes.${SORTED_KGTK} \

#     / tee $VERBOSE --use-mgzip=$USE_MGZIP \
#     --into-file ${DATADIR}/${PART}.properties.datatypes.${SORTED_KGTK} \

kgtk ${KGTK_FLAGS} \
     unique ${VERBOSE} --use-mgzip=$USE_MGZIP --presorted \
     --input-file ${DATADIR}/${PART}.properties.datatypes.${SORTED_KGTK} \
     --column node1 \
     --label datatype-count \
     --output-file ${DATADIR}/${PART}.properties.datatypes.counts.unsorted.${SORTED_KGTK} \

kgtk ${KGTK_FLAGS} \
     lift ${VERBOSE} --use-mgzip=${USE_MGZIP} \
     --input-file ${DATADIR}/${PART}.properties.datatypes.counts.unsorted.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${DATADIR}/${PART}.properties.datatypes.counts.lifted.${SORTED_KGTK}

kgtk ${KGTK_FLAGS} \
     sort2 ${VERBOSE} --use-mgzip=$USE_MGZIP --pure-python \
     --input-file ${DATADIR}/${PART}.properties.datatypes.counts.lifted.${SORTED_KGTK} \
     --columns node2 node1 label \
     --output-file ${DATADIR}/${PART}.properties.datatypes.counts.${SORTED_KGTK}
