#! /bin/bash

papermill \
    --progress-bar \
    --log-output --log-level DEBUG \
    partition-wikidata.ipynb \
    -p wikidata_input_path ./all.tsv.gz \
    -p wikidata_parts_path ./parts \
    -p temp_folder_path ./parts/temp \
    |& tee partition-wikidata.log
