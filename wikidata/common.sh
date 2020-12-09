#! /bin/bash

# This script expects to be executed with the current working directory.

# This is the Wikidata version we will analyze:
WIKIDATA_VERSION=wikidata-20201130
KGTK_WORK_DIR=/data3/rogers

# The `kgtk validate-properties` pattern files are expected to
# be in:
PATTERNDIR=/data1/rogers/kgtk/github/kgtk/wikidata/patterns

# This will be our working directory:
WIKIDATA_WORK_DIR=${KGTK_WORK_DIR}/kgtk/gd/kgtk_public_graphs/cache/${WIKIDATA_VERSION}

# The working data files will be stored in:
DATADIR=${WIKIDATA_WORK_DIR}/data

# Temporary files (unsorted) will be stored in in:
TEMPDIR=${WIKIDATA_WORK_DIR}/temp

# The working log files will be stored in:
LOGDIR=${WIKIDATA_WORK_DIR}/logs

# The count validation files will be stored in:
COUNTDIR=${WIKIDATA_WORK_DIR}/counts

# Completed data products will be stored in:
PRODUCTDIR=/data1/rogers/kgtk/gd/kgtk_public_graphs/drive/${WIKIDATA_VERSION}

# This script expects to see the wikidata dump JSON file in the
# following location:
WIKIDATA_JSON_DIR=${WIKIDATA_WORK_DIR}/dumps

# The Wikidata JSON file is named as follows:
WIKIDATA_ALL=${WIKIDATA_VERSION}-all
WIKIDATA_ALL_JSON=${WIKIDATA_JSON_DIR}/${WIKIDATA_ALL}.json.gz

# Work file extensions
UNSORTED_KGTK=unsorted.tsv.gz
SORTED_KGTK=tsv.gz

# Use mgzip in some cases?
USE_MGZIP=True

# Select on of the following gzip implementations:
# GZIP_CMD=gzip
GZIP_CMD=pigz

# Ensure that sort has enough space for its temporary files.
TMPDIR=${KGTK_WORK_DIR1}/tmp
export TMPDIR

# Skip cleaning for now.  When we enable it, we will need to adjust some file
# names in subsequent commands.
CLEAN=0

# Some common flags:
KGTK_FLAGS="--debug --timing --progress --progress-tty `tty`"
VERBOSE="--verbose"
SORT_EXTRAS="--parallel 24 --buffer-size 60% -T ${KGTK_WORK_DIR}/tmp"

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

# The wikidata import split files to be sorted:
WIKIDATA_IMPORT_SPLIT_FILES=( \
	"claims" \
	"claims.missingValues" \
	"qualifiers" \
	"qualifiers.missingValues" \
	"aliases" \
	"aliases.en" \
	"descriptions" \
	"descriptions.en" \
	"labels" \
	"labels.en" \
	"sitelinks" \
	"sitelinks.en" \
	"sitelinks.en.qualifiers" \
	"sitelinks.qualifiers" \
	"metadata.node" \
	"metadata.property.datatypes" \
	"metadata.types" \
    )
