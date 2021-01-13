This command performs calculations on one or more columns in a KGTK file. 
If no input filename is provided, the default is to read standard input. 

## Usage

```
usage: kgtk calc [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [-c [COLUMN_NAME [COLUMN_NAME ...]]] --into
                 INTO_COLUMN_NAMES [INTO_COLUMN_NAMES ...] --do {average,copy,join,percentage,set,sum}
                 [--values [VALUES [VALUES ...]]] [--format FORMAT_STRING] [-v [optional True|False]]

This command performs calculations on one or more columns in a KGTK file. 
If no input filename is provided, the default is to read standard input. 

Additional options are shown in expert help.
kgtk --expert rename_columns --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  -c [COLUMN_NAME [COLUMN_NAME ...]], --columns [COLUMN_NAME [COLUMN_NAME ...]]
                        The list of source column names, optionally containing '..' for column ranges and '...'
                        for column names not explicitly mentioned.
  --into INTO_COLUMN_NAMES [INTO_COLUMN_NAMES ...]
                        The name of the column to receive the result of the calculation.
  --do {average,copy,join,percentage,set,sum}
                        The name of the operation.
  --values [VALUES [VALUES ...]]
                        An optional list of values
  --format FORMAT_STRING
                        The format string for the calculation.

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:

| node1 | label | node2 | node1;total |
| -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 |
| P1000 | p585-count | 16 | 266 |
| P101 | p585-count | 5 | 157519 |
| P1018 | p585-count | 2 | 177 |
| P102 | p585-count | 295 | 414726 |
| P1025 | p585-count | 26 | 693 |
| P1026 | p585-count | 40 | 6930 |
| P1027 | p585-count | 14 | 10008 |
| P1028 | p585-count | 1131 | 4035 |
| P1029 | p585-count | 4 | 2643 |
| P1035 | p585-count | 4 | 366 |
| P1037 | p585-count | 60 | 9317 |
| P1040 | p585-count | 1 | 45073 |
| P1050 | p585-count | 246 | 226380 |
| P1056 | p585-count | 39 | 22414 |
| P106 | p585-count | 39933 | 6020911 |
| P1066 | p585-count | 53 | 36920 |
| P1071 | p585-count | 116 | 36143 |
| P1075 | p585-count | 2 | 1358 |
| P108 | p585-count | 729 | 790392 |
| P1081 | p585-count | 6816 | 12303 |
| P1082 | p585-count | 1416067 | 1476344 |
| P1083 | p585-count | 105 | 21347 |
| P1087 | p585-count | 2202513 | 2202513 |
| P109 | p585-count | 80 | 17448 |
| P1090 | p585-count | 2 | 946444 |
| P1092 | p585-count | 262 | 10322 |
| P1093 | p585-count | 6 | 28944 |
| P1096 | p585-count | 4 | 82897 |
| P1098 | p585-count | 885 | 1716 |
| P110 | p585-count | 18 | 8086 |
| P1103 | p585-count | 1 | 26706 |
| P1104 | p585-count | 9 | 105804 |
| P1110 | p585-count | 218 | 21359 |
| P1113 | p585-count | 149 | 51614 |
| P1114 | p585-count | 18002 | 23181 |
| P112 | p585-count | 225 | 51655 |
| P1120 | p585-count | 4657 | 11871 |
| P1125 | p585-count | 25 | 31 |
| P1128 | p585-count | 6503 | 12990 |
| P1132 | p585-count | 162 | 385048 |
| P1136 | p585-count | 11 | 100 |
| P1141 | p585-count | 2 | 10924 |
| P1142 | p585-count | 6 | 18106 |
| P115 | p585-count | 3 | 29020 |
| P1158 | p585-count | 1 | 449 |
| P1174 | p585-count | 31176 | 32246 |
| P118 | p585-count | 6 | 51646 |
| P1181 | p585-count | 33 | 10688 |
| P119 | p585-count | 1891 | 167837 |
| P1193 | p585-count | 47 | 86 |
| P1196 | p585-count | 9 | 78323 |
| P1198 | p585-count | 274 | 282 |
| P121 | p585-count | 285 | 8684 |
| P122 | p585-count | 12 | 1672 |
| P123 | p585-count | 149 | 213787 |
| P1234 | p585-count | 2 | 378 |
| P1240 | p585-count | 15224 | 17197 |
| P1243 | p585-count | 594 | 2971 |
| P1246 | p585-count | 3 | 1517 |
| P126 | p585-count | 1 | 292541 |
| P1268 | p585-count | 2 | 2056 |
| P1269 | p585-count | 2 | 77236 |
| P127 | p585-count | 1720 | 406984 |
| P1273 | p585-count | 1 | 45750 |
| P1274 | p585-count | 31 | 17333 |
| P1279 | p585-count | 5590 | 5591 |
| P1293 | p585-count | 50 | 62 |
| P1299 | p585-count | 34 | 2290 |
| P1303 | p585-count | 5 | 180254 |
| P1308 | p585-count | 25 | 10436 |
| P131 | p585-count | 527 | 9619445 |
| P1317 | p585-count | 2 | 17400 |
| P1318 | p585-count | 31 | 98 |
| P1325 | p585-count | 1 | 20659 |
| P1327 | p585-count | 12 | 7715 |
| P1329 | p585-count | 78 | 101546 |
| P1336 | p585-count | 5 | 1060 |
| P1339 | p585-count | 16 | 3341 |
| P1342 | p585-count | 2 | 7036 |
| P1343 | p585-count | 666 | 547692 |
| P1344 | p585-count | 2393 | 554130 |
| P1346 | p585-count | 29630 | 203745 |
| P1347 | p585-count | 7 | 7178 |
| P1350 | p585-count | 4241 | 34756 |
| P1351 | p585-count | 1 | 6147 |
| P1352 | p585-count | 60839 | 66049 |
| P1355 | p585-count | 1 | 27 |
| P1359 | p585-count | 229 | 231 |
| P136 | p585-count | 13 | 1189227 |
| P1365 | p585-count | 6989 | 43014 |
| P1366 | p585-count | 10357 | 46733 |
| P137 | p585-count | 194 | 458057 |
| P1373 | p585-count | 2330 | 2688 |
| P1376 | p585-count | 8 | 77905 |
| P138 | p585-count | 40 | 265751 |


Calculate the average of `node2` and `node1;total`:

```bash
kgtk calc -i kgtk/join/test/calc-file1.tsv -c node2 "node1;total" --into result --do average
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | 1976.00 |
| P1000 | p585-count | 16 | 266 | 141.00 |
| P101 | p585-count | 5 | 157519 | 78762.00 |
| P1018 | p585-count | 2 | 177 | 89.50 |
| P102 | p585-count | 295 | 414726 | 207510.50 |
| P1025 | p585-count | 26 | 693 | 359.50 |
| P1026 | p585-count | 40 | 6930 | 3485.00 |
| P1027 | p585-count | 14 | 10008 | 5011.00 |
| P1028 | p585-count | 1131 | 4035 | 2583.00 |
| P1029 | p585-count | 4 | 2643 | 1323.50 |
| P1035 | p585-count | 4 | 366 | 185.00 |
| P1037 | p585-count | 60 | 9317 | 4688.50 |
| P1040 | p585-count | 1 | 45073 | 22537.00 |
| P1050 | p585-count | 246 | 226380 | 113313.00 |
| P1056 | p585-count | 39 | 22414 | 11226.50 |
| P106 | p585-count | 39933 | 6020911 | 3030422.00 |
| P1066 | p585-count | 53 | 36920 | 18486.50 |
| P1071 | p585-count | 116 | 36143 | 18129.50 |
| P1075 | p585-count | 2 | 1358 | 680.00 |
| P108 | p585-count | 729 | 790392 | 395560.50 |
| P1081 | p585-count | 6816 | 12303 | 9559.50 |
| P1082 | p585-count | 1416067 | 1476344 | 1446205.50 |
| P1083 | p585-count | 105 | 21347 | 10726.00 |
| P1087 | p585-count | 2202513 | 2202513 | 2202513.00 |
| P109 | p585-count | 80 | 17448 | 8764.00 |
| P1090 | p585-count | 2 | 946444 | 473223.00 |
| P1092 | p585-count | 262 | 10322 | 5292.00 |
| P1093 | p585-count | 6 | 28944 | 14475.00 |
| P1096 | p585-count | 4 | 82897 | 41450.50 |
| P1098 | p585-count | 885 | 1716 | 1300.50 |
| P110 | p585-count | 18 | 8086 | 4052.00 |
| P1103 | p585-count | 1 | 26706 | 13353.50 |
| P1104 | p585-count | 9 | 105804 | 52906.50 |
| P1110 | p585-count | 218 | 21359 | 10788.50 |
| P1113 | p585-count | 149 | 51614 | 25881.50 |
| P1114 | p585-count | 18002 | 23181 | 20591.50 |
| P112 | p585-count | 225 | 51655 | 25940.00 |
| P1120 | p585-count | 4657 | 11871 | 8264.00 |
| P1125 | p585-count | 25 | 31 | 28.00 |
| P1128 | p585-count | 6503 | 12990 | 9746.50 |
| P1132 | p585-count | 162 | 385048 | 192605.00 |
| P1136 | p585-count | 11 | 100 | 55.50 |
| P1141 | p585-count | 2 | 10924 | 5463.00 |
| P1142 | p585-count | 6 | 18106 | 9056.00 |
| P115 | p585-count | 3 | 29020 | 14511.50 |
| P1158 | p585-count | 1 | 449 | 225.00 |
| P1174 | p585-count | 31176 | 32246 | 31711.00 |
| P118 | p585-count | 6 | 51646 | 25826.00 |
| P1181 | p585-count | 33 | 10688 | 5360.50 |
| P119 | p585-count | 1891 | 167837 | 84864.00 |
| P1193 | p585-count | 47 | 86 | 66.50 |
| P1196 | p585-count | 9 | 78323 | 39166.00 |
| P1198 | p585-count | 274 | 282 | 278.00 |
| P121 | p585-count | 285 | 8684 | 4484.50 |
| P122 | p585-count | 12 | 1672 | 842.00 |
| P123 | p585-count | 149 | 213787 | 106968.00 |
| P1234 | p585-count | 2 | 378 | 190.00 |
| P1240 | p585-count | 15224 | 17197 | 16210.50 |
| P1243 | p585-count | 594 | 2971 | 1782.50 |
| P1246 | p585-count | 3 | 1517 | 760.00 |
| P126 | p585-count | 1 | 292541 | 146271.00 |
| P1268 | p585-count | 2 | 2056 | 1029.00 |
| P1269 | p585-count | 2 | 77236 | 38619.00 |
| P127 | p585-count | 1720 | 406984 | 204352.00 |
| P1273 | p585-count | 1 | 45750 | 22875.50 |
| P1274 | p585-count | 31 | 17333 | 8682.00 |
| P1279 | p585-count | 5590 | 5591 | 5590.50 |
| P1293 | p585-count | 50 | 62 | 56.00 |
| P1299 | p585-count | 34 | 2290 | 1162.00 |
| P1303 | p585-count | 5 | 180254 | 90129.50 |
| P1308 | p585-count | 25 | 10436 | 5230.50 |
| P131 | p585-count | 527 | 9619445 | 4809986.00 |
| P1317 | p585-count | 2 | 17400 | 8701.00 |
| P1318 | p585-count | 31 | 98 | 64.50 |
| P1325 | p585-count | 1 | 20659 | 10330.00 |
| P1327 | p585-count | 12 | 7715 | 3863.50 |
| P1329 | p585-count | 78 | 101546 | 50812.00 |
| P1336 | p585-count | 5 | 1060 | 532.50 |
| P1339 | p585-count | 16 | 3341 | 1678.50 |
| P1342 | p585-count | 2 | 7036 | 3519.00 |
| P1343 | p585-count | 666 | 547692 | 274179.00 |
| P1344 | p585-count | 2393 | 554130 | 278261.50 |
| P1346 | p585-count | 29630 | 203745 | 116687.50 |
| P1347 | p585-count | 7 | 7178 | 3592.50 |
| P1350 | p585-count | 4241 | 34756 | 19498.50 |
| P1351 | p585-count | 1 | 6147 | 3074.00 |
| P1352 | p585-count | 60839 | 66049 | 63444.00 |
| P1355 | p585-count | 1 | 27 | 14.00 |
| P1359 | p585-count | 229 | 231 | 230.00 |
| P136 | p585-count | 13 | 1189227 | 594620.00 |
| P1365 | p585-count | 6989 | 43014 | 25001.50 |
| P1366 | p585-count | 10357 | 46733 | 28545.00 |
| P137 | p585-count | 194 | 458057 | 229125.50 |
| P1373 | p585-count | 2330 | 2688 | 2509.00 |
| P1376 | p585-count | 8 | 77905 | 38956.50 |
| P138 | p585-count | 40 | 265751 | 132895.50 |

Copy `node2` into the `node2-copy` column:

```bash
kgtk calc -i kgtk/join/test/calc-file1.tsv -c node2 --into node2-copy --do copy
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | node2-copy |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | 73 |
| P1000 | p585-count | 16 | 266 | 16 |
| P101 | p585-count | 5 | 157519 | 5 |
| P1018 | p585-count | 2 | 177 | 2 |
| P102 | p585-count | 295 | 414726 | 295 |
| P1025 | p585-count | 26 | 693 | 26 |
| P1026 | p585-count | 40 | 6930 | 40 |
| P1027 | p585-count | 14 | 10008 | 14 |
| P1028 | p585-count | 1131 | 4035 | 1131 |
| P1029 | p585-count | 4 | 2643 | 4 |
| P1035 | p585-count | 4 | 366 | 4 |
| P1037 | p585-count | 60 | 9317 | 60 |
| P1040 | p585-count | 1 | 45073 | 1 |
| P1050 | p585-count | 246 | 226380 | 246 |
| P1056 | p585-count | 39 | 22414 | 39 |
| P106 | p585-count | 39933 | 6020911 | 39933 |
| P1066 | p585-count | 53 | 36920 | 53 |
| P1071 | p585-count | 116 | 36143 | 116 |
| P1075 | p585-count | 2 | 1358 | 2 |
| P108 | p585-count | 729 | 790392 | 729 |
| P1081 | p585-count | 6816 | 12303 | 6816 |
| P1082 | p585-count | 1416067 | 1476344 | 1416067 |
| P1083 | p585-count | 105 | 21347 | 105 |
| P1087 | p585-count | 2202513 | 2202513 | 2202513 |
| P109 | p585-count | 80 | 17448 | 80 |
| P1090 | p585-count | 2 | 946444 | 2 |
| P1092 | p585-count | 262 | 10322 | 262 |
| P1093 | p585-count | 6 | 28944 | 6 |
| P1096 | p585-count | 4 | 82897 | 4 |
| P1098 | p585-count | 885 | 1716 | 885 |
| P110 | p585-count | 18 | 8086 | 18 |
| P1103 | p585-count | 1 | 26706 | 1 |
| P1104 | p585-count | 9 | 105804 | 9 |
| P1110 | p585-count | 218 | 21359 | 218 |
| P1113 | p585-count | 149 | 51614 | 149 |
| P1114 | p585-count | 18002 | 23181 | 18002 |
| P112 | p585-count | 225 | 51655 | 225 |
| P1120 | p585-count | 4657 | 11871 | 4657 |
| P1125 | p585-count | 25 | 31 | 25 |
| P1128 | p585-count | 6503 | 12990 | 6503 |
| P1132 | p585-count | 162 | 385048 | 162 |
| P1136 | p585-count | 11 | 100 | 11 |
| P1141 | p585-count | 2 | 10924 | 2 |
| P1142 | p585-count | 6 | 18106 | 6 |
| P115 | p585-count | 3 | 29020 | 3 |
| P1158 | p585-count | 1 | 449 | 1 |
| P1174 | p585-count | 31176 | 32246 | 31176 |
| P118 | p585-count | 6 | 51646 | 6 |
| P1181 | p585-count | 33 | 10688 | 33 |
| P119 | p585-count | 1891 | 167837 | 1891 |
| P1193 | p585-count | 47 | 86 | 47 |
| P1196 | p585-count | 9 | 78323 | 9 |
| P1198 | p585-count | 274 | 282 | 274 |
| P121 | p585-count | 285 | 8684 | 285 |
| P122 | p585-count | 12 | 1672 | 12 |
| P123 | p585-count | 149 | 213787 | 149 |
| P1234 | p585-count | 2 | 378 | 2 |
| P1240 | p585-count | 15224 | 17197 | 15224 |
| P1243 | p585-count | 594 | 2971 | 594 |
| P1246 | p585-count | 3 | 1517 | 3 |
| P126 | p585-count | 1 | 292541 | 1 |
| P1268 | p585-count | 2 | 2056 | 2 |
| P1269 | p585-count | 2 | 77236 | 2 |
| P127 | p585-count | 1720 | 406984 | 1720 |
| P1273 | p585-count | 1 | 45750 | 1 |
| P1274 | p585-count | 31 | 17333 | 31 |
| P1279 | p585-count | 5590 | 5591 | 5590 |
| P1293 | p585-count | 50 | 62 | 50 |
| P1299 | p585-count | 34 | 2290 | 34 |
| P1303 | p585-count | 5 | 180254 | 5 |
| P1308 | p585-count | 25 | 10436 | 25 |
| P131 | p585-count | 527 | 9619445 | 527 |
| P1317 | p585-count | 2 | 17400 | 2 |
| P1318 | p585-count | 31 | 98 | 31 |
| P1325 | p585-count | 1 | 20659 | 1 |
| P1327 | p585-count | 12 | 7715 | 12 |
| P1329 | p585-count | 78 | 101546 | 78 |
| P1336 | p585-count | 5 | 1060 | 5 |
| P1339 | p585-count | 16 | 3341 | 16 |
| P1342 | p585-count | 2 | 7036 | 2 |
| P1343 | p585-count | 666 | 547692 | 666 |
| P1344 | p585-count | 2393 | 554130 | 2393 |
| P1346 | p585-count | 29630 | 203745 | 29630 |
| P1347 | p585-count | 7 | 7178 | 7 |
| P1350 | p585-count | 4241 | 34756 | 4241 |
| P1351 | p585-count | 1 | 6147 | 1 |
| P1352 | p585-count | 60839 | 66049 | 60839 |
| P1355 | p585-count | 1 | 27 | 1 |
| P1359 | p585-count | 229 | 231 | 229 |
| P136 | p585-count | 13 | 1189227 | 13 |
| P1365 | p585-count | 6989 | 43014 | 6989 |
| P1366 | p585-count | 10357 | 46733 | 10357 |
| P137 | p585-count | 194 | 458057 | 194 |
| P1373 | p585-count | 2330 | 2688 | 2330 |
| P1376 | p585-count | 8 | 77905 | 8 |
| P138 | p585-count | 40 | 265751 | 40 |


Swap the `node2` and 'node1;total' column values:

```bash
kgtk calc -i kgtk/join/test/calc-file1.tsv -c node2 "node1;total" --into "node1;total" node2 --do copy
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total |
| -- | -- | -- | -- |
| P10 | p585-count | 3879 | 73 |
| P1000 | p585-count | 266 | 16 |
| P101 | p585-count | 157519 | 5 |
| P1018 | p585-count | 177 | 2 |
| P102 | p585-count | 414726 | 295 |
| P1025 | p585-count | 693 | 26 |
| P1026 | p585-count | 6930 | 40 |
| P1027 | p585-count | 10008 | 14 |
| P1028 | p585-count | 4035 | 1131 |
| P1029 | p585-count | 2643 | 4 |
| P1035 | p585-count | 366 | 4 |
| P1037 | p585-count | 9317 | 60 |
| P1040 | p585-count | 45073 | 1 |
| P1050 | p585-count | 226380 | 246 |
| P1056 | p585-count | 22414 | 39 |
| P106 | p585-count | 6020911 | 39933 |
| P1066 | p585-count | 36920 | 53 |
| P1071 | p585-count | 36143 | 116 |
| P1075 | p585-count | 1358 | 2 |
| P108 | p585-count | 790392 | 729 |
| P1081 | p585-count | 12303 | 6816 |
| P1082 | p585-count | 1476344 | 1416067 |
| P1083 | p585-count | 21347 | 105 |
| P1087 | p585-count | 2202513 | 2202513 |
| P109 | p585-count | 17448 | 80 |
| P1090 | p585-count | 946444 | 2 |
| P1092 | p585-count | 10322 | 262 |
| P1093 | p585-count | 28944 | 6 |
| P1096 | p585-count | 82897 | 4 |
| P1098 | p585-count | 1716 | 885 |
| P110 | p585-count | 8086 | 18 |
| P1103 | p585-count | 26706 | 1 |
| P1104 | p585-count | 105804 | 9 |
| P1110 | p585-count | 21359 | 218 |
| P1113 | p585-count | 51614 | 149 |
| P1114 | p585-count | 23181 | 18002 |
| P112 | p585-count | 51655 | 225 |
| P1120 | p585-count | 11871 | 4657 |
| P1125 | p585-count | 31 | 25 |
| P1128 | p585-count | 12990 | 6503 |
| P1132 | p585-count | 385048 | 162 |
| P1136 | p585-count | 100 | 11 |
| P1141 | p585-count | 10924 | 2 |
| P1142 | p585-count | 18106 | 6 |
| P115 | p585-count | 29020 | 3 |
| P1158 | p585-count | 449 | 1 |
| P1174 | p585-count | 32246 | 31176 |
| P118 | p585-count | 51646 | 6 |
| P1181 | p585-count | 10688 | 33 |
| P119 | p585-count | 167837 | 1891 |
| P1193 | p585-count | 86 | 47 |
| P1196 | p585-count | 78323 | 9 |
| P1198 | p585-count | 282 | 274 |
| P121 | p585-count | 8684 | 285 |
| P122 | p585-count | 1672 | 12 |
| P123 | p585-count | 213787 | 149 |
| P1234 | p585-count | 378 | 2 |
| P1240 | p585-count | 17197 | 15224 |
| P1243 | p585-count | 2971 | 594 |
| P1246 | p585-count | 1517 | 3 |
| P126 | p585-count | 292541 | 1 |
| P1268 | p585-count | 2056 | 2 |
| P1269 | p585-count | 77236 | 2 |
| P127 | p585-count | 406984 | 1720 |
| P1273 | p585-count | 45750 | 1 |
| P1274 | p585-count | 17333 | 31 |
| P1279 | p585-count | 5591 | 5590 |
| P1293 | p585-count | 62 | 50 |
| P1299 | p585-count | 2290 | 34 |
| P1303 | p585-count | 180254 | 5 |
| P1308 | p585-count | 10436 | 25 |
| P131 | p585-count | 9619445 | 527 |
| P1317 | p585-count | 17400 | 2 |
| P1318 | p585-count | 98 | 31 |
| P1325 | p585-count | 20659 | 1 |
| P1327 | p585-count | 7715 | 12 |
| P1329 | p585-count | 101546 | 78 |
| P1336 | p585-count | 1060 | 5 |
| P1339 | p585-count | 3341 | 16 |
| P1342 | p585-count | 7036 | 2 |
| P1343 | p585-count | 547692 | 666 |
| P1344 | p585-count | 554130 | 2393 |
| P1346 | p585-count | 203745 | 29630 |
| P1347 | p585-count | 7178 | 7 |
| P1350 | p585-count | 34756 | 4241 |
| P1351 | p585-count | 6147 | 1 |
| P1352 | p585-count | 66049 | 60839 |
| P1355 | p585-count | 27 | 1 |
| P1359 | p585-count | 231 | 229 |
| P136 | p585-count | 1189227 | 13 |
| P1365 | p585-count | 43014 | 6989 |
| P1366 | p585-count | 46733 | 10357 |
| P137 | p585-count | 458057 | 194 |
| P1373 | p585-count | 2688 | 2330 |
| P1376 | p585-count | 77905 | 8 |
| P138 | p585-count | 265751 | 40 |

Join the 'node1' and 'label' column values using ':' as a separator:

```bash
kgtk calc -i kgtk/join/test/calc-file1.tsv -c node1 label --value : --into result --do join
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | P10:p585-count |
| P1000 | p585-count | 16 | 266 | P1000:p585-count |
| P101 | p585-count | 5 | 157519 | P101:p585-count |
| P1018 | p585-count | 2 | 177 | P1018:p585-count |
| P102 | p585-count | 295 | 414726 | P102:p585-count |
| P1025 | p585-count | 26 | 693 | P1025:p585-count |
| P1026 | p585-count | 40 | 6930 | P1026:p585-count |
| P1027 | p585-count | 14 | 10008 | P1027:p585-count |
| P1028 | p585-count | 1131 | 4035 | P1028:p585-count |
| P1029 | p585-count | 4 | 2643 | P1029:p585-count |
| P1035 | p585-count | 4 | 366 | P1035:p585-count |
| P1037 | p585-count | 60 | 9317 | P1037:p585-count |
| P1040 | p585-count | 1 | 45073 | P1040:p585-count |
| P1050 | p585-count | 246 | 226380 | P1050:p585-count |
| P1056 | p585-count | 39 | 22414 | P1056:p585-count |
| P106 | p585-count | 39933 | 6020911 | P106:p585-count |
| P1066 | p585-count | 53 | 36920 | P1066:p585-count |
| P1071 | p585-count | 116 | 36143 | P1071:p585-count |
| P1075 | p585-count | 2 | 1358 | P1075:p585-count |
| P108 | p585-count | 729 | 790392 | P108:p585-count |
| P1081 | p585-count | 6816 | 12303 | P1081:p585-count |
| P1082 | p585-count | 1416067 | 1476344 | P1082:p585-count |
| P1083 | p585-count | 105 | 21347 | P1083:p585-count |
| P1087 | p585-count | 2202513 | 2202513 | P1087:p585-count |
| P109 | p585-count | 80 | 17448 | P109:p585-count |
| P1090 | p585-count | 2 | 946444 | P1090:p585-count |
| P1092 | p585-count | 262 | 10322 | P1092:p585-count |
| P1093 | p585-count | 6 | 28944 | P1093:p585-count |
| P1096 | p585-count | 4 | 82897 | P1096:p585-count |
| P1098 | p585-count | 885 | 1716 | P1098:p585-count |
| P110 | p585-count | 18 | 8086 | P110:p585-count |
| P1103 | p585-count | 1 | 26706 | P1103:p585-count |
| P1104 | p585-count | 9 | 105804 | P1104:p585-count |
| P1110 | p585-count | 218 | 21359 | P1110:p585-count |
| P1113 | p585-count | 149 | 51614 | P1113:p585-count |
| P1114 | p585-count | 18002 | 23181 | P1114:p585-count |
| P112 | p585-count | 225 | 51655 | P112:p585-count |
| P1120 | p585-count | 4657 | 11871 | P1120:p585-count |
| P1125 | p585-count | 25 | 31 | P1125:p585-count |
| P1128 | p585-count | 6503 | 12990 | P1128:p585-count |
| P1132 | p585-count | 162 | 385048 | P1132:p585-count |
| P1136 | p585-count | 11 | 100 | P1136:p585-count |
| P1141 | p585-count | 2 | 10924 | P1141:p585-count |
| P1142 | p585-count | 6 | 18106 | P1142:p585-count |
| P115 | p585-count | 3 | 29020 | P115:p585-count |
| P1158 | p585-count | 1 | 449 | P1158:p585-count |
| P1174 | p585-count | 31176 | 32246 | P1174:p585-count |
| P118 | p585-count | 6 | 51646 | P118:p585-count |
| P1181 | p585-count | 33 | 10688 | P1181:p585-count |
| P119 | p585-count | 1891 | 167837 | P119:p585-count |
| P1193 | p585-count | 47 | 86 | P1193:p585-count |
| P1196 | p585-count | 9 | 78323 | P1196:p585-count |
| P1198 | p585-count | 274 | 282 | P1198:p585-count |
| P121 | p585-count | 285 | 8684 | P121:p585-count |
| P122 | p585-count | 12 | 1672 | P122:p585-count |
| P123 | p585-count | 149 | 213787 | P123:p585-count |
| P1234 | p585-count | 2 | 378 | P1234:p585-count |
| P1240 | p585-count | 15224 | 17197 | P1240:p585-count |
| P1243 | p585-count | 594 | 2971 | P1243:p585-count |
| P1246 | p585-count | 3 | 1517 | P1246:p585-count |
| P126 | p585-count | 1 | 292541 | P126:p585-count |
| P1268 | p585-count | 2 | 2056 | P1268:p585-count |
| P1269 | p585-count | 2 | 77236 | P1269:p585-count |
| P127 | p585-count | 1720 | 406984 | P127:p585-count |
| P1273 | p585-count | 1 | 45750 | P1273:p585-count |
| P1274 | p585-count | 31 | 17333 | P1274:p585-count |
| P1279 | p585-count | 5590 | 5591 | P1279:p585-count |
| P1293 | p585-count | 50 | 62 | P1293:p585-count |
| P1299 | p585-count | 34 | 2290 | P1299:p585-count |
| P1303 | p585-count | 5 | 180254 | P1303:p585-count |
| P1308 | p585-count | 25 | 10436 | P1308:p585-count |
| P131 | p585-count | 527 | 9619445 | P131:p585-count |
| P1317 | p585-count | 2 | 17400 | P1317:p585-count |
| P1318 | p585-count | 31 | 98 | P1318:p585-count |
| P1325 | p585-count | 1 | 20659 | P1325:p585-count |
| P1327 | p585-count | 12 | 7715 | P1327:p585-count |
| P1329 | p585-count | 78 | 101546 | P1329:p585-count |
| P1336 | p585-count | 5 | 1060 | P1336:p585-count |
| P1339 | p585-count | 16 | 3341 | P1339:p585-count |
| P1342 | p585-count | 2 | 7036 | P1342:p585-count |
| P1343 | p585-count | 666 | 547692 | P1343:p585-count |
| P1344 | p585-count | 2393 | 554130 | P1344:p585-count |
| P1346 | p585-count | 29630 | 203745 | P1346:p585-count |
| P1347 | p585-count | 7 | 7178 | P1347:p585-count |
| P1350 | p585-count | 4241 | 34756 | P1350:p585-count |
| P1351 | p585-count | 1 | 6147 | P1351:p585-count |
| P1352 | p585-count | 60839 | 66049 | P1352:p585-count |
| P1355 | p585-count | 1 | 27 | P1355:p585-count |
| P1359 | p585-count | 229 | 231 | P1359:p585-count |
| P136 | p585-count | 13 | 1189227 | P136:p585-count |
| P1365 | p585-count | 6989 | 43014 | P1365:p585-count |
| P1366 | p585-count | 10357 | 46733 | P1366:p585-count |
| P137 | p585-count | 194 | 458057 | P137:p585-count |
| P1373 | p585-count | 2330 | 2688 | P1373:p585-count |
| P1376 | p585-count | 8 | 77905 | P1376:p585-count |
| P138 | p585-count | 40 | 265751 | P138:p585-count |

Calculate the percentage of `node2` and `node1;total`:

```bash
kgtk calc -i kgtk/join/test/calc-file1.tsv -c node2 "node1;total" --into result --do percentage
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 |  1.88 |
| P1000 | p585-count | 16 | 266 |  6.02 |
| P101 | p585-count | 5 | 157519 |  0.00 |
| P1018 | p585-count | 2 | 177 |  1.13 |
| P102 | p585-count | 295 | 414726 |  0.07 |
| P1025 | p585-count | 26 | 693 |  3.75 |
| P1026 | p585-count | 40 | 6930 |  0.58 |
| P1027 | p585-count | 14 | 10008 |  0.14 |
| P1028 | p585-count | 1131 | 4035 | 28.03 |
| P1029 | p585-count | 4 | 2643 |  0.15 |
| P1035 | p585-count | 4 | 366 |  1.09 |
| P1037 | p585-count | 60 | 9317 |  0.64 |
| P1040 | p585-count | 1 | 45073 |  0.00 |
| P1050 | p585-count | 246 | 226380 |  0.11 |
| P1056 | p585-count | 39 | 22414 |  0.17 |
| P106 | p585-count | 39933 | 6020911 |  0.66 |
| P1066 | p585-count | 53 | 36920 |  0.14 |
| P1071 | p585-count | 116 | 36143 |  0.32 |
| P1075 | p585-count | 2 | 1358 |  0.15 |
| P108 | p585-count | 729 | 790392 |  0.09 |
| P1081 | p585-count | 6816 | 12303 | 55.40 |
| P1082 | p585-count | 1416067 | 1476344 | 95.92 |
| P1083 | p585-count | 105 | 21347 |  0.49 |
| P1087 | p585-count | 2202513 | 2202513 | 100.00 |
| P109 | p585-count | 80 | 17448 |  0.46 |
| P1090 | p585-count | 2 | 946444 |  0.00 |
| P1092 | p585-count | 262 | 10322 |  2.54 |
| P1093 | p585-count | 6 | 28944 |  0.02 |
| P1096 | p585-count | 4 | 82897 |  0.00 |
| P1098 | p585-count | 885 | 1716 | 51.57 |
| P110 | p585-count | 18 | 8086 |  0.22 |
| P1103 | p585-count | 1 | 26706 |  0.00 |
| P1104 | p585-count | 9 | 105804 |  0.01 |
| P1110 | p585-count | 218 | 21359 |  1.02 |
| P1113 | p585-count | 149 | 51614 |  0.29 |
| P1114 | p585-count | 18002 | 23181 | 77.66 |
| P112 | p585-count | 225 | 51655 |  0.44 |
| P1120 | p585-count | 4657 | 11871 | 39.23 |
| P1125 | p585-count | 25 | 31 | 80.65 |
| P1128 | p585-count | 6503 | 12990 | 50.06 |
| P1132 | p585-count | 162 | 385048 |  0.04 |
| P1136 | p585-count | 11 | 100 | 11.00 |
| P1141 | p585-count | 2 | 10924 |  0.02 |
| P1142 | p585-count | 6 | 18106 |  0.03 |
| P115 | p585-count | 3 | 29020 |  0.01 |
| P1158 | p585-count | 1 | 449 |  0.22 |
| P1174 | p585-count | 31176 | 32246 | 96.68 |
| P118 | p585-count | 6 | 51646 |  0.01 |
| P1181 | p585-count | 33 | 10688 |  0.31 |
| P119 | p585-count | 1891 | 167837 |  1.13 |
| P1193 | p585-count | 47 | 86 | 54.65 |
| P1196 | p585-count | 9 | 78323 |  0.01 |
| P1198 | p585-count | 274 | 282 | 97.16 |
| P121 | p585-count | 285 | 8684 |  3.28 |
| P122 | p585-count | 12 | 1672 |  0.72 |
| P123 | p585-count | 149 | 213787 |  0.07 |
| P1234 | p585-count | 2 | 378 |  0.53 |
| P1240 | p585-count | 15224 | 17197 | 88.53 |
| P1243 | p585-count | 594 | 2971 | 19.99 |
| P1246 | p585-count | 3 | 1517 |  0.20 |
| P126 | p585-count | 1 | 292541 |  0.00 |
| P1268 | p585-count | 2 | 2056 |  0.10 |
| P1269 | p585-count | 2 | 77236 |  0.00 |
| P127 | p585-count | 1720 | 406984 |  0.42 |
| P1273 | p585-count | 1 | 45750 |  0.00 |
| P1274 | p585-count | 31 | 17333 |  0.18 |
| P1279 | p585-count | 5590 | 5591 | 99.98 |
| P1293 | p585-count | 50 | 62 | 80.65 |
| P1299 | p585-count | 34 | 2290 |  1.48 |
| P1303 | p585-count | 5 | 180254 |  0.00 |
| P1308 | p585-count | 25 | 10436 |  0.24 |
| P131 | p585-count | 527 | 9619445 |  0.01 |
| P1317 | p585-count | 2 | 17400 |  0.01 |
| P1318 | p585-count | 31 | 98 | 31.63 |
| P1325 | p585-count | 1 | 20659 |  0.00 |
| P1327 | p585-count | 12 | 7715 |  0.16 |
| P1329 | p585-count | 78 | 101546 |  0.08 |
| P1336 | p585-count | 5 | 1060 |  0.47 |
| P1339 | p585-count | 16 | 3341 |  0.48 |
| P1342 | p585-count | 2 | 7036 |  0.03 |
| P1343 | p585-count | 666 | 547692 |  0.12 |
| P1344 | p585-count | 2393 | 554130 |  0.43 |
| P1346 | p585-count | 29630 | 203745 | 14.54 |
| P1347 | p585-count | 7 | 7178 |  0.10 |
| P1350 | p585-count | 4241 | 34756 | 12.20 |
| P1351 | p585-count | 1 | 6147 |  0.02 |
| P1352 | p585-count | 60839 | 66049 | 92.11 |
| P1355 | p585-count | 1 | 27 |  3.70 |
| P1359 | p585-count | 229 | 231 | 99.13 |
| P136 | p585-count | 13 | 1189227 |  0.00 |
| P1365 | p585-count | 6989 | 43014 | 16.25 |
| P1366 | p585-count | 10357 | 46733 | 22.16 |
| P137 | p585-count | 194 | 458057 |  0.04 |
| P1373 | p585-count | 2330 | 2688 | 86.68 |
| P1376 | p585-count | 8 | 77905 |  0.01 |
| P138 | p585-count | 40 | 265751 |  0.02 |

Set a value into a column:

```bash
kgtk calc -i kgtk/join/test/calc-file1.tsv --value xxx --into result --do set
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | xxx |
| P1000 | p585-count | 16 | 266 | xxx |
| P101 | p585-count | 5 | 157519 | xxx |
| P1018 | p585-count | 2 | 177 | xxx |
| P102 | p585-count | 295 | 414726 | xxx |
| P1025 | p585-count | 26 | 693 | xxx |
| P1026 | p585-count | 40 | 6930 | xxx |
| P1027 | p585-count | 14 | 10008 | xxx |
| P1028 | p585-count | 1131 | 4035 | xxx |
| P1029 | p585-count | 4 | 2643 | xxx |
| P1035 | p585-count | 4 | 366 | xxx |
| P1037 | p585-count | 60 | 9317 | xxx |
| P1040 | p585-count | 1 | 45073 | xxx |
| P1050 | p585-count | 246 | 226380 | xxx |
| P1056 | p585-count | 39 | 22414 | xxx |
| P106 | p585-count | 39933 | 6020911 | xxx |
| P1066 | p585-count | 53 | 36920 | xxx |
| P1071 | p585-count | 116 | 36143 | xxx |
| P1075 | p585-count | 2 | 1358 | xxx |
| P108 | p585-count | 729 | 790392 | xxx |
| P1081 | p585-count | 6816 | 12303 | xxx |
| P1082 | p585-count | 1416067 | 1476344 | xxx |
| P1083 | p585-count | 105 | 21347 | xxx |
| P1087 | p585-count | 2202513 | 2202513 | xxx |
| P109 | p585-count | 80 | 17448 | xxx |
| P1090 | p585-count | 2 | 946444 | xxx |
| P1092 | p585-count | 262 | 10322 | xxx |
| P1093 | p585-count | 6 | 28944 | xxx |
| P1096 | p585-count | 4 | 82897 | xxx |
| P1098 | p585-count | 885 | 1716 | xxx |
| P110 | p585-count | 18 | 8086 | xxx |
| P1103 | p585-count | 1 | 26706 | xxx |
| P1104 | p585-count | 9 | 105804 | xxx |
| P1110 | p585-count | 218 | 21359 | xxx |
| P1113 | p585-count | 149 | 51614 | xxx |
| P1114 | p585-count | 18002 | 23181 | xxx |
| P112 | p585-count | 225 | 51655 | xxx |
| P1120 | p585-count | 4657 | 11871 | xxx |
| P1125 | p585-count | 25 | 31 | xxx |
| P1128 | p585-count | 6503 | 12990 | xxx |
| P1132 | p585-count | 162 | 385048 | xxx |
| P1136 | p585-count | 11 | 100 | xxx |
| P1141 | p585-count | 2 | 10924 | xxx |
| P1142 | p585-count | 6 | 18106 | xxx |
| P115 | p585-count | 3 | 29020 | xxx |
| P1158 | p585-count | 1 | 449 | xxx |
| P1174 | p585-count | 31176 | 32246 | xxx |
| P118 | p585-count | 6 | 51646 | xxx |
| P1181 | p585-count | 33 | 10688 | xxx |
| P119 | p585-count | 1891 | 167837 | xxx |
| P1193 | p585-count | 47 | 86 | xxx |
| P1196 | p585-count | 9 | 78323 | xxx |
| P1198 | p585-count | 274 | 282 | xxx |
| P121 | p585-count | 285 | 8684 | xxx |
| P122 | p585-count | 12 | 1672 | xxx |
| P123 | p585-count | 149 | 213787 | xxx |
| P1234 | p585-count | 2 | 378 | xxx |
| P1240 | p585-count | 15224 | 17197 | xxx |
| P1243 | p585-count | 594 | 2971 | xxx |
| P1246 | p585-count | 3 | 1517 | xxx |
| P126 | p585-count | 1 | 292541 | xxx |
| P1268 | p585-count | 2 | 2056 | xxx |
| P1269 | p585-count | 2 | 77236 | xxx |
| P127 | p585-count | 1720 | 406984 | xxx |
| P1273 | p585-count | 1 | 45750 | xxx |
| P1274 | p585-count | 31 | 17333 | xxx |
| P1279 | p585-count | 5590 | 5591 | xxx |
| P1293 | p585-count | 50 | 62 | xxx |
| P1299 | p585-count | 34 | 2290 | xxx |
| P1303 | p585-count | 5 | 180254 | xxx |
| P1308 | p585-count | 25 | 10436 | xxx |
| P131 | p585-count | 527 | 9619445 | xxx |
| P1317 | p585-count | 2 | 17400 | xxx |
| P1318 | p585-count | 31 | 98 | xxx |
| P1325 | p585-count | 1 | 20659 | xxx |
| P1327 | p585-count | 12 | 7715 | xxx |
| P1329 | p585-count | 78 | 101546 | xxx |
| P1336 | p585-count | 5 | 1060 | xxx |
| P1339 | p585-count | 16 | 3341 | xxx |
| P1342 | p585-count | 2 | 7036 | xxx |
| P1343 | p585-count | 666 | 547692 | xxx |
| P1344 | p585-count | 2393 | 554130 | xxx |
| P1346 | p585-count | 29630 | 203745 | xxx |
| P1347 | p585-count | 7 | 7178 | xxx |
| P1350 | p585-count | 4241 | 34756 | xxx |
| P1351 | p585-count | 1 | 6147 | xxx |
| P1352 | p585-count | 60839 | 66049 | xxx |
| P1355 | p585-count | 1 | 27 | xxx |
| P1359 | p585-count | 229 | 231 | xxx |
| P136 | p585-count | 13 | 1189227 | xxx |
| P1365 | p585-count | 6989 | 43014 | xxx |
| P1366 | p585-count | 10357 | 46733 | xxx |
| P137 | p585-count | 194 | 458057 | xxx |
| P1373 | p585-count | 2330 | 2688 | xxx |
| P1376 | p585-count | 8 | 77905 | xxx |
| P138 | p585-count | 40 | 265751 | xxx |

Calculate the sum of `node2` and `node1;total`:

```bash
kgtk calc -i kgtk/join/test/calc-file1.tsv -c node2 "node1;total" --into result --do sum
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | 3952.00 |
| P1000 | p585-count | 16 | 266 | 282.00 |
| P101 | p585-count | 5 | 157519 | 157524.00 |
| P1018 | p585-count | 2 | 177 | 179.00 |
| P102 | p585-count | 295 | 414726 | 415021.00 |
| P1025 | p585-count | 26 | 693 | 719.00 |
| P1026 | p585-count | 40 | 6930 | 6970.00 |
| P1027 | p585-count | 14 | 10008 | 10022.00 |
| P1028 | p585-count | 1131 | 4035 | 5166.00 |
| P1029 | p585-count | 4 | 2643 | 2647.00 |
| P1035 | p585-count | 4 | 366 | 370.00 |
| P1037 | p585-count | 60 | 9317 | 9377.00 |
| P1040 | p585-count | 1 | 45073 | 45074.00 |
| P1050 | p585-count | 246 | 226380 | 226626.00 |
| P1056 | p585-count | 39 | 22414 | 22453.00 |
| P106 | p585-count | 39933 | 6020911 | 6060844.00 |
| P1066 | p585-count | 53 | 36920 | 36973.00 |
| P1071 | p585-count | 116 | 36143 | 36259.00 |
| P1075 | p585-count | 2 | 1358 | 1360.00 |
| P108 | p585-count | 729 | 790392 | 791121.00 |
| P1081 | p585-count | 6816 | 12303 | 19119.00 |
| P1082 | p585-count | 1416067 | 1476344 | 2892411.00 |
| P1083 | p585-count | 105 | 21347 | 21452.00 |
| P1087 | p585-count | 2202513 | 2202513 | 4405026.00 |
| P109 | p585-count | 80 | 17448 | 17528.00 |
| P1090 | p585-count | 2 | 946444 | 946446.00 |
| P1092 | p585-count | 262 | 10322 | 10584.00 |
| P1093 | p585-count | 6 | 28944 | 28950.00 |
| P1096 | p585-count | 4 | 82897 | 82901.00 |
| P1098 | p585-count | 885 | 1716 | 2601.00 |
| P110 | p585-count | 18 | 8086 | 8104.00 |
| P1103 | p585-count | 1 | 26706 | 26707.00 |
| P1104 | p585-count | 9 | 105804 | 105813.00 |
| P1110 | p585-count | 218 | 21359 | 21577.00 |
| P1113 | p585-count | 149 | 51614 | 51763.00 |
| P1114 | p585-count | 18002 | 23181 | 41183.00 |
| P112 | p585-count | 225 | 51655 | 51880.00 |
| P1120 | p585-count | 4657 | 11871 | 16528.00 |
| P1125 | p585-count | 25 | 31 | 56.00 |
| P1128 | p585-count | 6503 | 12990 | 19493.00 |
| P1132 | p585-count | 162 | 385048 | 385210.00 |
| P1136 | p585-count | 11 | 100 | 111.00 |
| P1141 | p585-count | 2 | 10924 | 10926.00 |
| P1142 | p585-count | 6 | 18106 | 18112.00 |
| P115 | p585-count | 3 | 29020 | 29023.00 |
| P1158 | p585-count | 1 | 449 | 450.00 |
| P1174 | p585-count | 31176 | 32246 | 63422.00 |
| P118 | p585-count | 6 | 51646 | 51652.00 |
| P1181 | p585-count | 33 | 10688 | 10721.00 |
| P119 | p585-count | 1891 | 167837 | 169728.00 |
| P1193 | p585-count | 47 | 86 | 133.00 |
| P1196 | p585-count | 9 | 78323 | 78332.00 |
| P1198 | p585-count | 274 | 282 | 556.00 |
| P121 | p585-count | 285 | 8684 | 8969.00 |
| P122 | p585-count | 12 | 1672 | 1684.00 |
| P123 | p585-count | 149 | 213787 | 213936.00 |
| P1234 | p585-count | 2 | 378 | 380.00 |
| P1240 | p585-count | 15224 | 17197 | 32421.00 |
| P1243 | p585-count | 594 | 2971 | 3565.00 |
| P1246 | p585-count | 3 | 1517 | 1520.00 |
| P126 | p585-count | 1 | 292541 | 292542.00 |
| P1268 | p585-count | 2 | 2056 | 2058.00 |
| P1269 | p585-count | 2 | 77236 | 77238.00 |
| P127 | p585-count | 1720 | 406984 | 408704.00 |
| P1273 | p585-count | 1 | 45750 | 45751.00 |
| P1274 | p585-count | 31 | 17333 | 17364.00 |
| P1279 | p585-count | 5590 | 5591 | 11181.00 |
| P1293 | p585-count | 50 | 62 | 112.00 |
| P1299 | p585-count | 34 | 2290 | 2324.00 |
| P1303 | p585-count | 5 | 180254 | 180259.00 |
| P1308 | p585-count | 25 | 10436 | 10461.00 |
| P131 | p585-count | 527 | 9619445 | 9619972.00 |
| P1317 | p585-count | 2 | 17400 | 17402.00 |
| P1318 | p585-count | 31 | 98 | 129.00 |
| P1325 | p585-count | 1 | 20659 | 20660.00 |
| P1327 | p585-count | 12 | 7715 | 7727.00 |
| P1329 | p585-count | 78 | 101546 | 101624.00 |
| P1336 | p585-count | 5 | 1060 | 1065.00 |
| P1339 | p585-count | 16 | 3341 | 3357.00 |
| P1342 | p585-count | 2 | 7036 | 7038.00 |
| P1343 | p585-count | 666 | 547692 | 548358.00 |
| P1344 | p585-count | 2393 | 554130 | 556523.00 |
| P1346 | p585-count | 29630 | 203745 | 233375.00 |
| P1347 | p585-count | 7 | 7178 | 7185.00 |
| P1350 | p585-count | 4241 | 34756 | 38997.00 |
| P1351 | p585-count | 1 | 6147 | 6148.00 |
| P1352 | p585-count | 60839 | 66049 | 126888.00 |
| P1355 | p585-count | 1 | 27 | 28.00 |
| P1359 | p585-count | 229 | 231 | 460.00 |
| P136 | p585-count | 13 | 1189227 | 1189240.00 |
| P1365 | p585-count | 6989 | 43014 | 50003.00 |
| P1366 | p585-count | 10357 | 46733 | 57090.00 |
| P137 | p585-count | 194 | 458057 | 458251.00 |
| P1373 | p585-count | 2330 | 2688 | 5018.00 |
| P1376 | p585-count | 8 | 77905 | 77913.00 |
| P138 | p585-count | 40 | 265751 | 265791.00 |

Calculate the sum of `node2` and `node1;total`, with the result formatted as an integer:

```bash
kgtk calc -i kgtk/join/test/calc-file1.tsv -c node2 "node1;total" --into result --do sum --format '%d'
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | 3952 |
| P1000 | p585-count | 16 | 266 | 282 |
| P101 | p585-count | 5 | 157519 | 157524 |
| P1018 | p585-count | 2 | 177 | 179 |
| P102 | p585-count | 295 | 414726 | 415021 |
| P1025 | p585-count | 26 | 693 | 719 |
| P1026 | p585-count | 40 | 6930 | 6970 |
| P1027 | p585-count | 14 | 10008 | 10022 |
| P1028 | p585-count | 1131 | 4035 | 5166 |
| P1029 | p585-count | 4 | 2643 | 2647 |
| P1035 | p585-count | 4 | 366 | 370 |
| P1037 | p585-count | 60 | 9317 | 9377 |
| P1040 | p585-count | 1 | 45073 | 45074 |
| P1050 | p585-count | 246 | 226380 | 226626 |
| P1056 | p585-count | 39 | 22414 | 22453 |
| P106 | p585-count | 39933 | 6020911 | 6060844 |
| P1066 | p585-count | 53 | 36920 | 36973 |
| P1071 | p585-count | 116 | 36143 | 36259 |
| P1075 | p585-count | 2 | 1358 | 1360 |
| P108 | p585-count | 729 | 790392 | 791121 |
| P1081 | p585-count | 6816 | 12303 | 19119 |
| P1082 | p585-count | 1416067 | 1476344 | 2892411 |
| P1083 | p585-count | 105 | 21347 | 21452 |
| P1087 | p585-count | 2202513 | 2202513 | 4405026 |
| P109 | p585-count | 80 | 17448 | 17528 |
| P1090 | p585-count | 2 | 946444 | 946446 |
| P1092 | p585-count | 262 | 10322 | 10584 |
| P1093 | p585-count | 6 | 28944 | 28950 |
| P1096 | p585-count | 4 | 82897 | 82901 |
| P1098 | p585-count | 885 | 1716 | 2601 |
| P110 | p585-count | 18 | 8086 | 8104 |
| P1103 | p585-count | 1 | 26706 | 26707 |
| P1104 | p585-count | 9 | 105804 | 105813 |
| P1110 | p585-count | 218 | 21359 | 21577 |
| P1113 | p585-count | 149 | 51614 | 51763 |
| P1114 | p585-count | 18002 | 23181 | 41183 |
| P112 | p585-count | 225 | 51655 | 51880 |
| P1120 | p585-count | 4657 | 11871 | 16528 |
| P1125 | p585-count | 25 | 31 | 56 |
| P1128 | p585-count | 6503 | 12990 | 19493 |
| P1132 | p585-count | 162 | 385048 | 385210 |
| P1136 | p585-count | 11 | 100 | 111 |
| P1141 | p585-count | 2 | 10924 | 10926 |
| P1142 | p585-count | 6 | 18106 | 18112 |
| P115 | p585-count | 3 | 29020 | 29023 |
| P1158 | p585-count | 1 | 449 | 450 |
| P1174 | p585-count | 31176 | 32246 | 63422 |
| P118 | p585-count | 6 | 51646 | 51652 |
| P1181 | p585-count | 33 | 10688 | 10721 |
| P119 | p585-count | 1891 | 167837 | 169728 |
| P1193 | p585-count | 47 | 86 | 133 |
| P1196 | p585-count | 9 | 78323 | 78332 |
| P1198 | p585-count | 274 | 282 | 556 |
| P121 | p585-count | 285 | 8684 | 8969 |
| P122 | p585-count | 12 | 1672 | 1684 |
| P123 | p585-count | 149 | 213787 | 213936 |
| P1234 | p585-count | 2 | 378 | 380 |
| P1240 | p585-count | 15224 | 17197 | 32421 |
| P1243 | p585-count | 594 | 2971 | 3565 |
| P1246 | p585-count | 3 | 1517 | 1520 |
| P126 | p585-count | 1 | 292541 | 292542 |
| P1268 | p585-count | 2 | 2056 | 2058 |
| P1269 | p585-count | 2 | 77236 | 77238 |
| P127 | p585-count | 1720 | 406984 | 408704 |
| P1273 | p585-count | 1 | 45750 | 45751 |
| P1274 | p585-count | 31 | 17333 | 17364 |
| P1279 | p585-count | 5590 | 5591 | 11181 |
| P1293 | p585-count | 50 | 62 | 112 |
| P1299 | p585-count | 34 | 2290 | 2324 |
| P1303 | p585-count | 5 | 180254 | 180259 |
| P1308 | p585-count | 25 | 10436 | 10461 |
| P131 | p585-count | 527 | 9619445 | 9619972 |
| P1317 | p585-count | 2 | 17400 | 17402 |
| P1318 | p585-count | 31 | 98 | 129 |
| P1325 | p585-count | 1 | 20659 | 20660 |
| P1327 | p585-count | 12 | 7715 | 7727 |
| P1329 | p585-count | 78 | 101546 | 101624 |
| P1336 | p585-count | 5 | 1060 | 1065 |
| P1339 | p585-count | 16 | 3341 | 3357 |
| P1342 | p585-count | 2 | 7036 | 7038 |
| P1343 | p585-count | 666 | 547692 | 548358 |
| P1344 | p585-count | 2393 | 554130 | 556523 |
| P1346 | p585-count | 29630 | 203745 | 233375 |
| P1347 | p585-count | 7 | 7178 | 7185 |
| P1350 | p585-count | 4241 | 34756 | 38997 |
| P1351 | p585-count | 1 | 6147 | 6148 |
| P1352 | p585-count | 60839 | 66049 | 126888 |
| P1355 | p585-count | 1 | 27 | 28 |
| P1359 | p585-count | 229 | 231 | 460 |
| P136 | p585-count | 13 | 1189227 | 1189240 |
| P1365 | p585-count | 6989 | 43014 | 50003 |
| P1366 | p585-count | 10357 | 46733 | 57090 |
| P137 | p585-count | 194 | 458057 | 458251 |
| P1373 | p585-count | 2330 | 2688 | 5018 |
| P1376 | p585-count | 8 | 77905 | 77913 |
| P138 | p585-count | 40 | 265751 | 265791 |
