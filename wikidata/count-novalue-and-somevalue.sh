#! /bin/bash

source common.sh

echo -e "\nCount the occurances of the missing value indicators ('novalue', 'somevalue') in the node2 column in ${DATADIR}/claims.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP  \
     --input-file $DATADIR/claims.$SORTED_KGTK \
     -p ';; novalue,somevalue' -o - \
     / unique ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --column node2 \
     --label novalue-count \
     --output-file ${COUNTDIR}/claims.node2.missingvalue.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/claims.node2.missingvalue.counts.log

echo -e "\nCount the occurances of the missing value indicators ('novalue', 'somevalue') in the node2 column in ${DATADIR}/qualifiers.${SORTED_KGTK}."
kgtk ${KGTK_FLAGS} \
     filter $VERBOSE --use-mgzip=$USE_MGZIP  \
     --input-file $DATADIR/qualifiers.$SORTED_KGTK \
     -p ';; novalue,somevalue' -o - \
     / unique ${VERBOSE} --use-mgzip=$USE_MGZIP \
     --column node2 \
     --label novalue-count \
     --output-file ${COUNTDIR}/qualifiers.node2.missingvalue.counts.${SORTED_KGTK} \
     |& tee ${LOGDIR}/qualifiers.node2.missingvalue.counts.log

