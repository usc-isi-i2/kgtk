#! /bin/bash

papermill \
    --progress-bar \
    --log-output --log-level DEBUG \
    partition-wikidata.ipynb \
    |& tee partition-wikidata.log
