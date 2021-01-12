This command performs calculations on one or more columns in a KGTK file. 
If no input filename is provided, the default is to read standard input. 

## Usage

```
usage: kgtk calc [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] -c COLUMN_NAME [COLUMN_NAME ...] --into INTO_COLUMN_NAME --do {average,percentage,sum}
                 [--format FORMAT_STRING] [-v]

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
  -c COLUMN_NAME [COLUMN_NAME ...], --columns COLUMN_NAME [COLUMN_NAME ...]
                        The list of source column names, optionally containing '..' for column ranges and '...' for column names not explicitly mentioned.
  --into INTO_COLUMN_NAME
                        The name of the column to receive the result of the calculation.
  --do {average,percentage,sum}
                        The name of the operation.
  --format FORMAT_STRING
                        The format string for the calculation.

  -v, --verbose         Print additional progress messages (default=False).
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
