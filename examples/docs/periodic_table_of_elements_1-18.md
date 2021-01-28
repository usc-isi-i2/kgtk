# Periodic Table of the First 18 Elements

These files are based on a [GitHub project by Goodman Sciences](https://gist.github.com/GoodmanSciences/c2dd862cd38f21b0ad36b8f96b4bf1ee.js).

The data was downloaded on 27-Jan-2021.  It was reformatted as follows:

## periodic_table_of_elements.csv

 * Only the fist 18 data rows were retained.
 * Independent discovers were indicated by `|`.
 * Discovery teams had spaces replaced by `_`.

## periodic_table_of_elements.tsv

In addition to the changes listed above, the following changes were made:

 * Commas were replaced by tabs in `periodic_table_of_elements.tsv`
 * An `id` column was inserted at the front of each row,
   * with a copy of the element's symbol.
