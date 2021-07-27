## Overview

Convert one or more TDM JSON files to a KGTK file.

The TDM (Trade Data Monitor) data come in a JSON file downloaded from
a query for a specific country and its major trading partners.
The query must specify an annual time series where each year starts
in January.

The input file is supposed to come from a URL similar to the following:

https://www1.tdmlogin.com/tdm/api/profile.aspmethod=getRecordSet&hs=01&rpt=BR&rpt_options=N&lang=EN&fmt=annual&flow=I&listby=Partner&period=202012&periodplus=&ptn=&ptn_cgoptions=&currency=USD&qv=V&selqty=QTY1&userid=5335&cgroup=&qconv=0&product=&directto=0&diff=1&orderColumn=V6&orderDirection=DESC&drill=0&isRightClick=false

The output contains records listing the type of goods processed, with
qualifiers specifying the trading partner and the dollar amount.

Thge type of goods are specified by a Harmonized System Code,
which is a string that heirarchically encodes the type of goods.

## Usage
```
usage: kgtk import-tdm [-h] [-i INPUT_FILE [INPUT_FILE ...]] [-o OUTPUT_FILE]
                       [--old-id-column-name COLUMN_NAME]
                       [--new-id-column-name COLUMN_NAME]
                       [--overwrite-id [optional true|false]]
                       [--verify-id-unique [optional true|false]]
                       [--id-style {node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,empty,prefix###,wikidata,wikidata-with-claim-id}]
                       [--id-prefix PREFIX] [--initial-id INTEGER]
                       [--id-prefix-num-width INTEGER]
                       [--id-concat-num-width INTEGER]
                       [--value-hash-width VALUE_HASH_WIDTH]
                       [--claim-id-hash-width CLAIM_ID_HASH_WIDTH]
                       [--claim-id-column-name CLAIM_ID_COLUMN_NAME]
                       [--id-separator ID_SEPARATOR]
                       [-v [optional True|False]]

Convert a TDM JSON input file to a KGTK file on output.

Additional options are shown in expert help.
kgtk --expert import-tdm --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE [INPUT_FILE ...], --input-files INPUT_FILE [INPUT_FILE ...]
                        The TDM JSON file to import. (May be omitted or '-'
                        for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK file to write. (May be omitted or '-' for
                        stdout.)
  --old-id-column-name COLUMN_NAME
                        The name of the old ID column. (default=id).
  --new-id-column-name COLUMN_NAME
                        The name of the new ID column. (default=id).
  --overwrite-id [optional true|false]
                        When true, replace existing ID values. When false,
                        copy existing ID values. When --overwrite-id is
                        omitted, it defaults to False. When --overwrite-id is
                        supplied without an argument, it is True.
  --verify-id-unique [optional true|false]
                        When true, verify ID uniqueness using an in-memory set
                        of IDs. When --verify-id-unique is omitted, it
                        defaults to False. When --verify-id-unique is supplied
                        without an argument, it is True.
  --id-style {node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,empty,prefix###,wikidata,wikidata-with-claim-id}
                        The ID generation style. (default=empty).
  --id-prefix PREFIX    The prefix for a prefix### ID. (default=E).
  --initial-id INTEGER  The initial numeric value for a prefix### ID.
                        (default=1).
  --id-prefix-num-width INTEGER
                        The width of the numeric value for a prefix### ID.
                        (default=1).
  --id-concat-num-width INTEGER
                        The width of the numeric value for a concatenated ID.
                        (default=4).
  --value-hash-width VALUE_HASH_WIDTH
                        How many characters should be used in a value hash?
                        (default=6)
  --claim-id-hash-width CLAIM_ID_HASH_WIDTH
                        How many characters should be used to hash the claim
                        ID? 0 means do not hash the claim ID. (default=8)
  --claim-id-column-name CLAIM_ID_COLUMN_NAME
                        The name of the claim_id column. (default=claim_id)
  --id-separator ID_SEPARATOR
                        The separator user between ID subfields. (default=-)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Sample File with Feedback

Process a sample file with verbose feedback.  By default, an `id` column will
be include din the output file but ID values will not be generated.

```bash
kgtk import-tdm --verbose \
     -i examples/docs/import-tdm-example1.json \
     -o import-tdm-example1.tsv
```

Here are the feedback messages:

    File_path.suffix: .tsv
    KgtkWriter: writing file import-tdm-example1.tsv
    header: id	node1	label	node2	P17	P585	PTDMmonetary_value	P248
    File 1: processing 'examples/docs/import-tdm-example1.json'
    36 trading partners processed, 252 cells imported.
    1 harmonized system codes processed
    38 labels processed

Here is the output file:

```bash
kgtk cat -i import-tdm-example1.tsv
```

| id | node1 | label | node2 | P17 | P585 | PTDMmonetary_value | P248 |
| -- | -- | -- | -- | -- | -- | -- | -- |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2015-01-01T00:00:00/9 | 2316869Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2016-01-01T00:00:00/9 | 2071673Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2017-01-01T00:00:00/9 | 3749942Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2018-01-01T00:00:00/9 | 3361673Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2019-01-01T00:00:00/9 | 3017655Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2020-01-01T00:00:00/9 | 2769939Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2021-01-01T00:00:00/9 | 17287751Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2015-01-01T00:00:00/9 | 81169Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2016-01-01T00:00:00/9 | 760838Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2017-01-01T00:00:00/9 | 5409Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2018-01-01T00:00:00/9 | 346040Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2019-01-01T00:00:00/9 | 77940Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2020-01-01T00:00:00/9 | 993563Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2021-01-01T00:00:00/9 | 2264959Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2015-01-01T00:00:00/9 | 258825Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2016-01-01T00:00:00/9 | 2284687Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2017-01-01T00:00:00/9 | 272993Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2018-01-01T00:00:00/9 | 147752Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2019-01-01T00:00:00/9 | 1696683Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2020-01-01T00:00:00/9 | 818059Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2021-01-01T00:00:00/9 | 5478999Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2015-01-01T00:00:00/9 | 313969Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2016-01-01T00:00:00/9 | 314210Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2017-01-01T00:00:00/9 | 313236Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2018-01-01T00:00:00/9 | 95Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2019-01-01T00:00:00/9 | 1153372Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2020-01-01T00:00:00/9 | 658164Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2021-01-01T00:00:00/9 | 2753046Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2015-01-01T00:00:00/9 | 1502119Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2016-01-01T00:00:00/9 | 1003363Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2017-01-01T00:00:00/9 | 603320Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2018-01-01T00:00:00/9 | 1159705Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2019-01-01T00:00:00/9 | 1038345Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2020-01-01T00:00:00/9 | 534996Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2021-01-01T00:00:00/9 | 5841848Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2015-01-01T00:00:00/9 | 150191Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2016-01-01T00:00:00/9 | 130486Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2017-01-01T00:00:00/9 | 1326665Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2018-01-01T00:00:00/9 | 3089921Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2019-01-01T00:00:00/9 | 4096040Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2020-01-01T00:00:00/9 | 425390Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2021-01-01T00:00:00/9 | 9218693Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2015-01-01T00:00:00/9 | 656751Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2016-01-01T00:00:00/9 | 2238119Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2017-01-01T00:00:00/9 | 986214Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2018-01-01T00:00:00/9 | 69947Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2019-01-01T00:00:00/9 | 1343100Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2020-01-01T00:00:00/9 | 339743Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2021-01-01T00:00:00/9 | 5633874Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2015-01-01T00:00:00/9 | 125890Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2016-01-01T00:00:00/9 | 156915Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2017-01-01T00:00:00/9 | 426695Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2018-01-01T00:00:00/9 | 99825Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2019-01-01T00:00:00/9 | 127981Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2020-01-01T00:00:00/9 | 114194Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2021-01-01T00:00:00/9 | 1051500Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2015-01-01T00:00:00/9 | 1631376Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2016-01-01T00:00:00/9 | 1322147Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2017-01-01T00:00:00/9 | 465102Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2018-01-01T00:00:00/9 | 640900Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2019-01-01T00:00:00/9 | 511966Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2020-01-01T00:00:00/9 | 78286Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2021-01-01T00:00:00/9 | 4649777Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2020-01-01T00:00:00/9 | 60000Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2021-01-01T00:00:00/9 | 60000Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2015-01-01T00:00:00/9 | 17289Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2016-01-01T00:00:00/9 | 224213Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2017-01-01T00:00:00/9 | 15991Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2018-01-01T00:00:00/9 | 213500Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2019-01-01T00:00:00/9 | 495070Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2020-01-01T00:00:00/9 | 34011Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2021-01-01T00:00:00/9 | 1000074Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2016-01-01T00:00:00/9 | 300000Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2017-01-01T00:00:00/9 | 550000Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2020-01-01T00:00:00/9 | 16890Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2021-01-01T00:00:00/9 | 866890Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2017-01-01T00:00:00/9 | 1123Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2018-01-01T00:00:00/9 | 1442Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2020-01-01T00:00:00/9 | 9340Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2021-01-01T00:00:00/9 | 11905Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2020-01-01T00:00:00/9 | 7167Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2021-01-01T00:00:00/9 | 7167Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2015-01-01T00:00:00/9 | 20080Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2016-01-01T00:00:00/9 | 13000Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2017-01-01T00:00:00/9 | 19500Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2018-01-01T00:00:00/9 | 63000Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2019-01-01T00:00:00/9 | 15792Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2020-01-01T00:00:00/9 | 7000Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2021-01-01T00:00:00/9 | 138372Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2015-01-01T00:00:00/9 | 1517505Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2016-01-01T00:00:00/9 | 1906592Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2017-01-01T00:00:00/9 | 134765Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2018-01-01T00:00:00/9 | 48808Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2019-01-01T00:00:00/9 | 46322Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2020-01-01T00:00:00/9 | 6600Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2021-01-01T00:00:00/9 | 3660592Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2017-01-01T00:00:00/9 | 6051Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2020-01-01T00:00:00/9 | 5353Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2021-01-01T00:00:00/9 | 11404Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2015-01-01T00:00:00/9 | 114805Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2016-01-01T00:00:00/9 | 102755Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2017-01-01T00:00:00/9 | 49886Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2018-01-01T00:00:00/9 | 261631Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2019-01-01T00:00:00/9 | 24703Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2020-01-01T00:00:00/9 | 4769Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2021-01-01T00:00:00/9 | 558549Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2015-01-01T00:00:00/9 | 1071Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2016-01-01T00:00:00/9 | 31885Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2017-01-01T00:00:00/9 | 46485Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2018-01-01T00:00:00/9 | 2356Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2019-01-01T00:00:00/9 | 44457Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2020-01-01T00:00:00/9 | 2901Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2021-01-01T00:00:00/9 | 129155Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2015-01-01T00:00:00/9 | 1390955Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2017-01-01T00:00:00/9 | 568Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2018-01-01T00:00:00/9 | 67062Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2019-01-01T00:00:00/9 | 15263Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2020-01-01T00:00:00/9 | 2801Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2021-01-01T00:00:00/9 | 1476649Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2020-01-01T00:00:00/9 | 800Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2021-01-01T00:00:00/9 | 800Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2017-01-01T00:00:00/9 | 23496Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2020-01-01T00:00:00/9 | 30Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2021-01-01T00:00:00/9 | 23526Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2017-01-01T00:00:00/9 | 3182Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2021-01-01T00:00:00/9 | 3182Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2016-01-01T00:00:00/9 | 2719Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2021-01-01T00:00:00/9 | 2719Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2017-01-01T00:00:00/9 | 15000Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2018-01-01T00:00:00/9 | 27000Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2021-01-01T00:00:00/9 | 42000Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2015-01-01T00:00:00/9 | 11163Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2021-01-01T00:00:00/9 | 11163Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2015-01-01T00:00:00/9 | 1280Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2016-01-01T00:00:00/9 | 3514Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2018-01-01T00:00:00/9 | 12392Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2019-01-01T00:00:00/9 | 3324Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2021-01-01T00:00:00/9 | 20510Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2015-01-01T00:00:00/9 | 39753Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2021-01-01T00:00:00/9 | 39753Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2015-01-01T00:00:00/9 | 10540Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2021-01-01T00:00:00/9 | 10540Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2016-01-01T00:00:00/9 | 2201Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2021-01-01T00:00:00/9 | 2201Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2015-01-01T00:00:00/9 | 920Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2021-01-01T00:00:00/9 | 920Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2015-01-01T00:00:00/9 | 1463Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2016-01-01T00:00:00/9 | 4522Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2017-01-01T00:00:00/9 | 1093Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2021-01-01T00:00:00/9 | 7078Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2016-01-01T00:00:00/9 | 587Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2021-01-01T00:00:00/9 | 587Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2015-01-01T00:00:00/9 | 22851Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2016-01-01T00:00:00/9 | 7279Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2021-01-01T00:00:00/9 | 30130Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2015-01-01T00:00:00/9 | 30805Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2016-01-01T00:00:00/9 | 21188Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2017-01-01T00:00:00/9 | 31980Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2021-01-01T00:00:00/9 | 83973Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2019-01-01T00:00:00/9 | 3920Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
|  | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2021-01-01T00:00:00/9 | 3920Q4917 | Q97355106 |
|  | QTDM_HS_01 | P5471 | "01" |  |  |  |  |
|  | QTDM_HS_01 | label | 'Live Animals'@en |  |  |  |  |
|  | QTDM_country_Argentina | label | 'Argentina'@en |  |  |  |  |
|  | QTDM_country_Australia | label | 'Australia'@en |  |  |  |  |
|  | QTDM_country_Austria | label | 'Austria'@en |  |  |  |  |
|  | QTDM_country_Barbados | label | 'Barbados'@en |  |  |  |  |
|  | QTDM_country_Belgium | label | 'Belgium'@en |  |  |  |  |
|  | QTDM_country_Bermuda | label | 'Bermuda'@en |  |  |  |  |
|  | QTDM_country_Brazil | label | 'Brazil'@en |  |  |  |  |
|  | QTDM_country_British_Virgin_Islands | label | 'British Virgin Islands'@en |  |  |  |  |
|  | QTDM_country_Canada | label | 'Canada'@en |  |  |  |  |
|  | QTDM_country_Canary_Isles | label | 'Canary Isles'@en |  |  |  |  |
|  | QTDM_country_Chile | label | 'Chile'@en |  |  |  |  |
|  | QTDM_country_Colombia | label | 'Colombia'@en |  |  |  |  |
|  | QTDM_country_Czech_Republic | label | 'Czech Republic'@en |  |  |  |  |
|  | QTDM_country_Denmark | label | 'Denmark'@en |  |  |  |  |
|  | QTDM_country_Estonia | label | 'Estonia'@en |  |  |  |  |
|  | QTDM_country_Finland | label | 'Finland'@en |  |  |  |  |
|  | QTDM_country_France | label | 'France'@en |  |  |  |  |
|  | QTDM_country_Germany | label | 'Germany'@en |  |  |  |  |
|  | QTDM_country_Hungary | label | 'Hungary'@en |  |  |  |  |
|  | QTDM_country_Indonesia | label | 'Indonesia'@en |  |  |  |  |
|  | QTDM_country_Ireland | label | 'Ireland'@en |  |  |  |  |
|  | QTDM_country_Italy | label | 'Italy'@en |  |  |  |  |
|  | QTDM_country_Japan | label | 'Japan'@en |  |  |  |  |
|  | QTDM_country_Netherlands | label | 'Netherlands'@en |  |  |  |  |
|  | QTDM_country_New_Zealand | label | 'New Zealand'@en |  |  |  |  |
|  | QTDM_country_Portugal | label | 'Portugal'@en |  |  |  |  |
|  | QTDM_country_Russia | label | 'Russia'@en |  |  |  |  |
|  | QTDM_country_Slovakia | label | 'Slovakia'@en |  |  |  |  |
|  | QTDM_country_South_Africa | label | 'South Africa'@en |  |  |  |  |
|  | QTDM_country_Spain | label | 'Spain'@en |  |  |  |  |
|  | QTDM_country_Sweden | label | 'Sweden'@en |  |  |  |  |
|  | QTDM_country_Thailand | label | 'Thailand'@en |  |  |  |  |
|  | QTDM_country_United_Arab_Emirates | label | 'United Arab Emirates'@en |  |  |  |  |
|  | QTDM_country_United_Kingdom | label | 'United Kingdom'@en |  |  |  |  |
|  | QTDM_country_United_States | label | 'United States'@en |  |  |  |  |
|  | QTDM_country_Uruguay | label | 'Uruguay'@en |  |  |  |  |
|  | QTDM_iso_country_BR | label | 'Brazil'@en |  |  |  |  |

### Building IDs

ID values may be built during processing.  Due to the HS code and label edges,
ID values should be generated only if all JSON input files are processed at
the same time.

```bash
kgtk import-tdm \
     -i examples/docs/import-tdm-example1.json \
     --id-style node1-label-node2-num
```

| id | node1 | label | node2 | P17 | P585 | PTDMmonetary_value | P248 |
| -- | -- | -- | -- | -- | -- | -- | -- |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0000 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2015-01-01T00:00:00/9 | 2316869Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0001 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2016-01-01T00:00:00/9 | 2071673Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0002 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2017-01-01T00:00:00/9 | 3749942Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0003 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2018-01-01T00:00:00/9 | 3361673Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0004 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2019-01-01T00:00:00/9 | 3017655Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0005 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2020-01-01T00:00:00/9 | 2769939Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0006 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_States | ^2021-01-01T00:00:00/9 | 17287751Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0007 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2015-01-01T00:00:00/9 | 81169Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0008 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2016-01-01T00:00:00/9 | 760838Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0009 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2017-01-01T00:00:00/9 | 5409Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0010 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2018-01-01T00:00:00/9 | 346040Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0011 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2019-01-01T00:00:00/9 | 77940Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0012 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2020-01-01T00:00:00/9 | 993563Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0013 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Kingdom | ^2021-01-01T00:00:00/9 | 2264959Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0014 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2015-01-01T00:00:00/9 | 258825Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0015 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2016-01-01T00:00:00/9 | 2284687Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0016 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2017-01-01T00:00:00/9 | 272993Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0017 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2018-01-01T00:00:00/9 | 147752Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0018 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2019-01-01T00:00:00/9 | 1696683Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0019 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2020-01-01T00:00:00/9 | 818059Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0020 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Netherlands | ^2021-01-01T00:00:00/9 | 5478999Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0021 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2015-01-01T00:00:00/9 | 313969Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0022 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2016-01-01T00:00:00/9 | 314210Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0023 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2017-01-01T00:00:00/9 | 313236Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0024 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2018-01-01T00:00:00/9 | 95Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0025 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2019-01-01T00:00:00/9 | 1153372Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0026 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2020-01-01T00:00:00/9 | 658164Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0027 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Denmark | ^2021-01-01T00:00:00/9 | 2753046Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0028 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2015-01-01T00:00:00/9 | 1502119Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0029 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2016-01-01T00:00:00/9 | 1003363Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0030 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2017-01-01T00:00:00/9 | 603320Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0031 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2018-01-01T00:00:00/9 | 1159705Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0032 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2019-01-01T00:00:00/9 | 1038345Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0033 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2020-01-01T00:00:00/9 | 534996Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0034 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Belgium | ^2021-01-01T00:00:00/9 | 5841848Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0035 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2015-01-01T00:00:00/9 | 150191Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0036 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2016-01-01T00:00:00/9 | 130486Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0037 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2017-01-01T00:00:00/9 | 1326665Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0038 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2018-01-01T00:00:00/9 | 3089921Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0039 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2019-01-01T00:00:00/9 | 4096040Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0040 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2020-01-01T00:00:00/9 | 425390Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0041 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canada | ^2021-01-01T00:00:00/9 | 9218693Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0042 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2015-01-01T00:00:00/9 | 656751Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0043 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2016-01-01T00:00:00/9 | 2238119Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0044 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2017-01-01T00:00:00/9 | 986214Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0045 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2018-01-01T00:00:00/9 | 69947Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0046 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2019-01-01T00:00:00/9 | 1343100Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0047 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2020-01-01T00:00:00/9 | 339743Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0048 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Germany | ^2021-01-01T00:00:00/9 | 5633874Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0049 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2015-01-01T00:00:00/9 | 125890Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0050 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2016-01-01T00:00:00/9 | 156915Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0051 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2017-01-01T00:00:00/9 | 426695Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0052 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2018-01-01T00:00:00/9 | 99825Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0053 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2019-01-01T00:00:00/9 | 127981Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0054 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2020-01-01T00:00:00/9 | 114194Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0055 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Argentina | ^2021-01-01T00:00:00/9 | 1051500Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0056 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2015-01-01T00:00:00/9 | 1631376Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0057 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2016-01-01T00:00:00/9 | 1322147Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0058 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2017-01-01T00:00:00/9 | 465102Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0059 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2018-01-01T00:00:00/9 | 640900Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0060 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2019-01-01T00:00:00/9 | 511966Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0061 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2020-01-01T00:00:00/9 | 78286Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0062 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_France | ^2021-01-01T00:00:00/9 | 4649777Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0063 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0064 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0065 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0066 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0067 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0068 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2020-01-01T00:00:00/9 | 60000Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0069 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Colombia | ^2021-01-01T00:00:00/9 | 60000Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0070 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2015-01-01T00:00:00/9 | 17289Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0071 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2016-01-01T00:00:00/9 | 224213Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0072 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2017-01-01T00:00:00/9 | 15991Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0073 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2018-01-01T00:00:00/9 | 213500Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0074 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2019-01-01T00:00:00/9 | 495070Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0075 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2020-01-01T00:00:00/9 | 34011Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0076 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Ireland | ^2021-01-01T00:00:00/9 | 1000074Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0077 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0078 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2016-01-01T00:00:00/9 | 300000Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0079 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2017-01-01T00:00:00/9 | 550000Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0080 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0081 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0082 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2020-01-01T00:00:00/9 | 16890Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0083 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_British_Virgin_Islands | ^2021-01-01T00:00:00/9 | 866890Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0084 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0085 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0086 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2017-01-01T00:00:00/9 | 1123Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0087 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2018-01-01T00:00:00/9 | 1442Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0088 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0089 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2020-01-01T00:00:00/9 | 9340Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0090 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Austria | ^2021-01-01T00:00:00/9 | 11905Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0091 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0092 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0093 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0094 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0095 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0096 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2020-01-01T00:00:00/9 | 7167Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0097 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_United_Arab_Emirates | ^2021-01-01T00:00:00/9 | 7167Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0098 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2015-01-01T00:00:00/9 | 20080Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0099 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2016-01-01T00:00:00/9 | 13000Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0100 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2017-01-01T00:00:00/9 | 19500Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0101 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2018-01-01T00:00:00/9 | 63000Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0102 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2019-01-01T00:00:00/9 | 15792Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0103 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2020-01-01T00:00:00/9 | 7000Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0104 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Brazil | ^2021-01-01T00:00:00/9 | 138372Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0105 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2015-01-01T00:00:00/9 | 1517505Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0106 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2016-01-01T00:00:00/9 | 1906592Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0107 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2017-01-01T00:00:00/9 | 134765Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0108 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2018-01-01T00:00:00/9 | 48808Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0109 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2019-01-01T00:00:00/9 | 46322Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0110 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2020-01-01T00:00:00/9 | 6600Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0111 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Uruguay | ^2021-01-01T00:00:00/9 | 3660592Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0112 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0113 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0114 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2017-01-01T00:00:00/9 | 6051Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0115 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0116 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0117 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2020-01-01T00:00:00/9 | 5353Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0118 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Hungary | ^2021-01-01T00:00:00/9 | 11404Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0119 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2015-01-01T00:00:00/9 | 114805Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0120 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2016-01-01T00:00:00/9 | 102755Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0121 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2017-01-01T00:00:00/9 | 49886Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0122 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2018-01-01T00:00:00/9 | 261631Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0123 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2019-01-01T00:00:00/9 | 24703Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0124 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2020-01-01T00:00:00/9 | 4769Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0125 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Portugal | ^2021-01-01T00:00:00/9 | 558549Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0126 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2015-01-01T00:00:00/9 | 1071Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0127 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2016-01-01T00:00:00/9 | 31885Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0128 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2017-01-01T00:00:00/9 | 46485Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0129 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2018-01-01T00:00:00/9 | 2356Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0130 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2019-01-01T00:00:00/9 | 44457Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0131 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2020-01-01T00:00:00/9 | 2901Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0132 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Italy | ^2021-01-01T00:00:00/9 | 129155Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0133 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2015-01-01T00:00:00/9 | 1390955Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0134 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0135 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2017-01-01T00:00:00/9 | 568Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0136 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2018-01-01T00:00:00/9 | 67062Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0137 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2019-01-01T00:00:00/9 | 15263Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0138 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2020-01-01T00:00:00/9 | 2801Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0139 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Spain | ^2021-01-01T00:00:00/9 | 1476649Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0140 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0141 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0142 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0143 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0144 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0145 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2020-01-01T00:00:00/9 | 800Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0146 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Russia | ^2021-01-01T00:00:00/9 | 800Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0147 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0148 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0149 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2017-01-01T00:00:00/9 | 23496Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0150 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0151 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0152 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2020-01-01T00:00:00/9 | 30Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0153 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Czech_Republic | ^2021-01-01T00:00:00/9 | 23526Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0154 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0155 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0156 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2017-01-01T00:00:00/9 | 3182Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0157 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0158 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0159 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0160 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Estonia | ^2021-01-01T00:00:00/9 | 3182Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0161 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0162 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2016-01-01T00:00:00/9 | 2719Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0163 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0164 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0165 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0166 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0167 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Finland | ^2021-01-01T00:00:00/9 | 2719Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0168 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0169 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0170 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2017-01-01T00:00:00/9 | 15000Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0171 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2018-01-01T00:00:00/9 | 27000Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0172 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0173 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0174 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Chile | ^2021-01-01T00:00:00/9 | 42000Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0175 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2015-01-01T00:00:00/9 | 11163Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0176 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0177 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0178 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0179 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0180 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0181 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Canary_Isles | ^2021-01-01T00:00:00/9 | 11163Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0182 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2015-01-01T00:00:00/9 | 1280Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0183 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2016-01-01T00:00:00/9 | 3514Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0184 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0185 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2018-01-01T00:00:00/9 | 12392Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0186 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2019-01-01T00:00:00/9 | 3324Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0187 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0188 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Australia | ^2021-01-01T00:00:00/9 | 20510Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0189 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2015-01-01T00:00:00/9 | 39753Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0190 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0191 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0192 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0193 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0194 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0195 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Barbados | ^2021-01-01T00:00:00/9 | 39753Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0196 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2015-01-01T00:00:00/9 | 10540Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0197 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0198 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0199 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0200 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0201 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0202 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Bermuda | ^2021-01-01T00:00:00/9 | 10540Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0203 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0204 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2016-01-01T00:00:00/9 | 2201Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0205 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0206 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0207 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0208 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0209 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Slovakia | ^2021-01-01T00:00:00/9 | 2201Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0210 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2015-01-01T00:00:00/9 | 920Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0211 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0212 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0213 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0214 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0215 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0216 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Sweden | ^2021-01-01T00:00:00/9 | 920Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0217 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2015-01-01T00:00:00/9 | 1463Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0218 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2016-01-01T00:00:00/9 | 4522Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0219 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2017-01-01T00:00:00/9 | 1093Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0220 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0221 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0222 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0223 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Thailand | ^2021-01-01T00:00:00/9 | 7078Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0224 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0225 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2016-01-01T00:00:00/9 | 587Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0226 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0227 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0228 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0229 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0230 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Japan | ^2021-01-01T00:00:00/9 | 587Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0231 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2015-01-01T00:00:00/9 | 22851Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0232 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2016-01-01T00:00:00/9 | 7279Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0233 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0234 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0235 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0236 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0237 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_New_Zealand | ^2021-01-01T00:00:00/9 | 30130Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0238 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2015-01-01T00:00:00/9 | 30805Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0239 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2016-01-01T00:00:00/9 | 21188Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0240 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2017-01-01T00:00:00/9 | 31980Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0241 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0242 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2019-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0243 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0244 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_South_Africa | ^2021-01-01T00:00:00/9 | 83973Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0245 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2015-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0246 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2016-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0247 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2017-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0248 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2018-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0249 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2019-01-01T00:00:00/9 | 3920Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0250 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2020-01-01T00:00:00/9 | 0Q4917 | Q97355106 |
| QTDM_iso_country_BR-PTDM_goods_imported-QTDM_HS_01-0251 | QTDM_iso_country_BR | PTDM_goods_imported | QTDM_HS_01 | QTDM_country_Indonesia | ^2021-01-01T00:00:00/9 | 3920Q4917 | Q97355106 |
| QTDM_HS_01-P5471-"01"-0000 | QTDM_HS_01 | P5471 | "01" |  |  |  |  |
| QTDM_HS_01-label-'Live Animals'@en-0000 | QTDM_HS_01 | label | 'Live Animals'@en |  |  |  |  |
| QTDM_country_Argentina-label-'Argentina'@en-0000 | QTDM_country_Argentina | label | 'Argentina'@en |  |  |  |  |
| QTDM_country_Australia-label-'Australia'@en-0000 | QTDM_country_Australia | label | 'Australia'@en |  |  |  |  |
| QTDM_country_Austria-label-'Austria'@en-0000 | QTDM_country_Austria | label | 'Austria'@en |  |  |  |  |
| QTDM_country_Barbados-label-'Barbados'@en-0000 | QTDM_country_Barbados | label | 'Barbados'@en |  |  |  |  |
| QTDM_country_Belgium-label-'Belgium'@en-0000 | QTDM_country_Belgium | label | 'Belgium'@en |  |  |  |  |
| QTDM_country_Bermuda-label-'Bermuda'@en-0000 | QTDM_country_Bermuda | label | 'Bermuda'@en |  |  |  |  |
| QTDM_country_Brazil-label-'Brazil'@en-0000 | QTDM_country_Brazil | label | 'Brazil'@en |  |  |  |  |
| QTDM_country_British_Virgin_Islands-label-'British Virgin Islands'@en-0000 | QTDM_country_British_Virgin_Islands | label | 'British Virgin Islands'@en |  |  |  |  |
| QTDM_country_Canada-label-'Canada'@en-0000 | QTDM_country_Canada | label | 'Canada'@en |  |  |  |  |
| QTDM_country_Canary_Isles-label-'Canary Isles'@en-0000 | QTDM_country_Canary_Isles | label | 'Canary Isles'@en |  |  |  |  |
| QTDM_country_Chile-label-'Chile'@en-0000 | QTDM_country_Chile | label | 'Chile'@en |  |  |  |  |
| QTDM_country_Colombia-label-'Colombia'@en-0000 | QTDM_country_Colombia | label | 'Colombia'@en |  |  |  |  |
| QTDM_country_Czech_Republic-label-'Czech Republic'@en-0000 | QTDM_country_Czech_Republic | label | 'Czech Republic'@en |  |  |  |  |
| QTDM_country_Denmark-label-'Denmark'@en-0000 | QTDM_country_Denmark | label | 'Denmark'@en |  |  |  |  |
| QTDM_country_Estonia-label-'Estonia'@en-0000 | QTDM_country_Estonia | label | 'Estonia'@en |  |  |  |  |
| QTDM_country_Finland-label-'Finland'@en-0000 | QTDM_country_Finland | label | 'Finland'@en |  |  |  |  |
| QTDM_country_France-label-'France'@en-0000 | QTDM_country_France | label | 'France'@en |  |  |  |  |
| QTDM_country_Germany-label-'Germany'@en-0000 | QTDM_country_Germany | label | 'Germany'@en |  |  |  |  |
| QTDM_country_Hungary-label-'Hungary'@en-0000 | QTDM_country_Hungary | label | 'Hungary'@en |  |  |  |  |
| QTDM_country_Indonesia-label-'Indonesia'@en-0000 | QTDM_country_Indonesia | label | 'Indonesia'@en |  |  |  |  |
| QTDM_country_Ireland-label-'Ireland'@en-0000 | QTDM_country_Ireland | label | 'Ireland'@en |  |  |  |  |
| QTDM_country_Italy-label-'Italy'@en-0000 | QTDM_country_Italy | label | 'Italy'@en |  |  |  |  |
| QTDM_country_Japan-label-'Japan'@en-0000 | QTDM_country_Japan | label | 'Japan'@en |  |  |  |  |
| QTDM_country_Netherlands-label-'Netherlands'@en-0000 | QTDM_country_Netherlands | label | 'Netherlands'@en |  |  |  |  |
| QTDM_country_New_Zealand-label-'New Zealand'@en-0000 | QTDM_country_New_Zealand | label | 'New Zealand'@en |  |  |  |  |
| QTDM_country_Portugal-label-'Portugal'@en-0000 | QTDM_country_Portugal | label | 'Portugal'@en |  |  |  |  |
| QTDM_country_Russia-label-'Russia'@en-0000 | QTDM_country_Russia | label | 'Russia'@en |  |  |  |  |
| QTDM_country_Slovakia-label-'Slovakia'@en-0000 | QTDM_country_Slovakia | label | 'Slovakia'@en |  |  |  |  |
| QTDM_country_South_Africa-label-'South Africa'@en-0000 | QTDM_country_South_Africa | label | 'South Africa'@en |  |  |  |  |
| QTDM_country_Spain-label-'Spain'@en-0000 | QTDM_country_Spain | label | 'Spain'@en |  |  |  |  |
| QTDM_country_Sweden-label-'Sweden'@en-0000 | QTDM_country_Sweden | label | 'Sweden'@en |  |  |  |  |
| QTDM_country_Thailand-label-'Thailand'@en-0000 | QTDM_country_Thailand | label | 'Thailand'@en |  |  |  |  |
| QTDM_country_United_Arab_Emirates-label-'United Arab Emirates'@en-0000 | QTDM_country_United_Arab_Emirates | label | 'United Arab Emirates'@en |  |  |  |  |
| QTDM_country_United_Kingdom-label-'United Kingdom'@en-0000 | QTDM_country_United_Kingdom | label | 'United Kingdom'@en |  |  |  |  |
| QTDM_country_United_States-label-'United States'@en-0000 | QTDM_country_United_States | label | 'United States'@en |  |  |  |  |
| QTDM_country_Uruguay-label-'Uruguay'@en-0000 | QTDM_country_Uruguay | label | 'Uruguay'@en |  |  |  |  |
| QTDM_iso_country_BR-label-'Brazil'@en-0000 | QTDM_iso_country_BR | label | 'Brazil'@en |  |  |  |  |
