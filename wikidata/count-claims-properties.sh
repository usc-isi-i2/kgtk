#! /bin/bash

source common.sh

echo -e "\nCount the properties in the node1 column in ${DATADIR}/claims.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file $DATADIR/claims.$SORTED_KGTK \
     -p '^P.*$ ;;' -o - \
     / unique ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --column node1 \
     --label node1-property-count \
     / lift ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/claims.node1.property.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     |& tee ${LOGDIR}/claims.node1.property.counts.log

echo -e "\nCount the properties in the label column in ${DATADIR}/claims.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file $DATADIR/claims.$SORTED_KGTK \
     -p '; ^P.*$ ;' -o - \
     / unique ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --column label \
     --label label-property-count \
     / lift ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/claims.label.property.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     |& tee ${LOGDIR}/claims.label.property.counts.log

echo -e "\nCount the properties in the node2 column in ${DATADIR}/claims.${SORTED_KGTK} and lift English labels."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP --regex \
     --input-file $DATADIR/claims.$SORTED_KGTK \
     -p ';; ^P.*$' -o - \
     / unique ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --column node2 \
     --label node2-property-count \
     / lift ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --label-file ${DATADIR}/labels.en.${SORTED_KGTK} \
     --output-file ${DATADIR}/claims.node2.property.counts.${SORTED_KGTK} \
     --columns-to-lift node1 \
     --input-file-is-presorted \
     --label-file-is-presorted \
     |& tee ${LOGDIR}/claims.node2.property.counts.log

