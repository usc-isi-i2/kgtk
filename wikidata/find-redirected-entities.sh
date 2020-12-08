#! /bin/sh

kgtk --debug --timing --progress \
     extract-wikidata-json \
     --input-file /data3/rogers/kgtk/gd/kgtk/cache/datasets/wikidata-20200803/json/wikidata-20200803-all.json.gz \
     --use-mgzip-for-input=False \
     --output-file redirected-entities.json \
     --find \
     Q16963368 \
     Q2376264 \
     Q5406494 \
     Q50263283 \
     Q3801563 \
     Q2513166 \
     Q21923992 \
     Q12694582\
     Q6330434 \
     Q24725604 \
     Q27796629 \
     Q85803429 \
     Q133421 \
     Q24768287 \
     Q57897486 \
     Q20481199 \
     Q7916883 \
     Q24784390\
     Q6422240 \
     Q1400881 \
     Q50694621 \
     Q25509593 \
     Q66091357 \
     Q2531594 \
     Q1326070 \
     Q998627 \
     
