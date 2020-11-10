#! /bin/bash

source common.sh

kgtk ${KGTK_FLAGS} \
     cat ${VERBOSE} --use-mgzip \
     -i /data4/rogers/elicit/cache/datasets/wikidata-20200803/data/all.tsv.gz \
     -i /data4/rogers/elicit/cache/datasets/wikidata-20200803/data/qual.tsv.gz \
     -i /data4/rogers/elicit/cache/datasets/wikidata-20200803/data/part.alias.tsv.gz \
     -i /data4/rogers/elicit/cache/datasets/wikidata-20200803/data/part.description.tsv.gz \
     -i /data4/rogers/elicit/cache/datasets/wikidata-20200803/data/part.label.tsv.gz \
     -i /data4/rogers/elicit/cache/datasets/wikidata-20200803/data/part.wikipedia_sitelink.tsv.gz \
     -i /data4/rogers/elicit/cache/datasets/wikidata-20200803/data/types.tsv.gz \
     -i /data4/rogers/elicit/cache/datasets/wikidata-20200803/data/property.datatype.tsv.gz \
     -o /data4/rogers/elicit/cache/datasets/wikidata-20200803/data/everything.tsv.gz \


