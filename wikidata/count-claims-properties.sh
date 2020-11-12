#! /bin/bash

source common.sh

echo -e "\nCount the properties in the node1 column in ${DATADIR}/claims.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file $DATADIR/claims.$SORTED_KGTK \
     -p '^P.*$ ;;' -o - \
     unique ${VERBOSE} \
     --output-file ${DATADIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --column node1 \
     --label node1-property-count \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/claims.node1.property.counts.log

echo -e "\nCount the properties in the label column in ${DATADIR}/claims.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file $DATADIR/claims.$SORTED_KGTK \
     -p '; ^P.*$ ;' -o - \
     unique ${VERBOSE} \
     --output-file ${DATADIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --column label \
     --label label-property-count \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/claims.label.property.counts.log

echo -e "\nCount the properties in the node2 column in ${DATADIR}/claims.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file $DATADIR/claims.$SORTED_KGTK \
     -p ';; ^P.*$' -o - \
     unique ${VERBOSE} \
     --output-file ${DATADIR}/claims.node2.property.counts.${SORTED_KGTK} \
     --column node2 \
     --label node2-property-count \
     --use-mgzip ${USE_MGZIP} \
     |& tee ${LOGDIR}/claims.node2.property.counts.log

