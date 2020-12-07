#! /bin/bash

source common.sh

# ==============================================================================
echo -e "\nCount the properties in the node1 column in ${DATADIR}/all.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/all.${SORTED_KGTK} \
     -p '^P[^-]*$ ;;' -o - \
     / unique ${VERBOSE} --use-mgzip=$USE_MGZIP --presorted \
     --column node1 \
     --label node1-property-count \
     / lift ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/all.node1.property.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/all.node1.property.counts.log

echo -e "\nCount the properties in the label column in ${DATADIR}/all.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/all.${SORTED_KGTK} \
     -p '; ^P[^-]*$ ;' -o - \
     / unique ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --column label \
     --label label-property-count \
     / lift ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/all.label.property.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/all.label.property.counts.log

echo -e "\nCount the properties in the node2 column in ${DATADIR}/all.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file ${DATADIR}/all.${SORTED_KGTK} \
     -p ';; ^P[^-]*$' -o - \
     / unique ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --column node2 \
     --label node2-property-count \
     / lift ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/all.node2.property.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/all.node2.propertycounts.log
