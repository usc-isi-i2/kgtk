#! /bin/bash

# This script expects to be executed with the current working directory.

# This is the Wikidata version we will analyze:
WIKIDATA_VERSION=wikidata-20200803

KGTK_WORK_DIR1=/data3/rogers
KGTK_WORK_DIR2=/data4/rogers

# This script expects to see the wikidata dump JSON file in the
# following location:
WIKIDATA_JSON_DIR=${KGTK_WORK_DIR1}/elicit/cache/datasets/${WIKIDATA_VERSION}

# The `kgtk validate-properties` pattern files are expected to
# be in:
PATTERNDIR=/data1/rogers/elicit/github/kgtk/wikidata/patterns

# This will be our working directory:
WIKIDATA_WORK_DIR=${KGTK_WORK_DIR2}/elicit/cache/datasets/${WIKIDATA_VERSION}

# The working data files will be stored in:
DATADIR=${WIKIDATA_WORK_DIR}/data

# The working log files will be stored in:
LOGDIR=${WIKIDATA_WORK_DIR}/logs

# Completed data products will be stored in:
PRODUCTDIR=/data1/rogers/elicit/drive/datasets/${WIKIDATA_VERSION}-v4

# The Wikidata JSON file is named as follows:
WIKIDATA_ALL=${WIKIDATA_VERSION}-all
WIKIDATA_ALL_JSON=${WIKIDATA_JSON_DIR}/${WIKIDATA_ALL}.json.gz

# We will import the following files first:
WIKIDATA_ALL_NODES=${WIKIDATA_ALL}-nodes # a node file
WIKIDATA_ALL_EDGES=${WIKIDATA_ALL}-edges # the main edge file
WIKIDATA_ALL_QUALIFIERS=${WIKIDATA_ALL}-qualifiers # the qualifiers

# Work file extensions
UNSORTED_KGTK=unsorted.tsv
SORTED_KGTK=tsv.gz

# Use mgzip in some cases?
USE_MGZIP=True

# Ensure that sort has enough space for its temporary files.
TMPDIR=${KGTK_WORK_DIR1}/tmp
export TMPDIR

# Skip cleaning for now.  When we enable it, we will need to adjust some file
# names in subsequent commands.
CLEAN=0

# Some common flags:
KGTK_FLAGS="--debug --timing --progress --progress-tty `tty`"
VERBOSE="--verbose"
SORT_EXTRAS="--parallel 24 --buffer-size 75% -T ${KGTK_WORK_DIR1}/tmp -T ${KGTK_WORK_DIR2}/tmp"

# The Wikidata datatypes:
WIKIDATATYPES=( \
	    "commonsMedia" \
		"external-id" \
		"geo-shape" \
		"globe-coordinate" \
		"math" \
		"monolingualtext" \
		"musical-notation" \
		"quantity" \
		"string" \
		"tabular-data" \
		"time" \
		"url" \
		"wikibase-form" \
		"wikibase-item" \
		"wikibase-lexeme" \
		"wikibase-property" \
		"wikibase-sense" \
		"other" \
    )

# The wikidata import split files:
WIKIDATA_IMPORT_SPLIT_FILES=( \
    "node" \
	"all.full" \
	"all" \
	"qual.full" \
	"qual" \
	"part.alias" \
	"part.alias.en" \
	"part.description" \
	"part.description.en" \
	"part.label" \
	"part.label.en" \
	"property.datatype" \
	"types" \
	"part.wikipedia_sitelink" \
	"part.wikipedia_sitelink.en" \
	"part.property" \
	"part.property.qual" \
    )

# GZIP_CMD=gzip
GZIP_CMD=pigz
