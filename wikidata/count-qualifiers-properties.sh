#! /bin/bash

source common.sh

echo -e "\nCount the properties in the label column in ${DATADIR}/qualifiers.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file $DATADIR/qualifiers.$SORTED_KGTK \
     -p '; ^P ;' -o - \
     / unique ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --column label \
     --label label-property-count \
     / lift ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/qualifiers.label.property.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/qualifiers.label.property.counts.log

echo -e "\nCount the properties in the node2 column in ${DATADIR}/qualifiers.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file $DATADIR/qualifiers.$SORTED_KGTK \
     -p ';; ^P' -o - \
     / unique ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --column node2 \
     --label node2-property-count \
     / lift ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --input-file-is-presorted \
     --columns-to-lift node1 \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --label-file-is-presorted \
     --output-file ${COUNTDIR}/qualifiers.node2.property.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/qualifiers.node2.property.counts.log

