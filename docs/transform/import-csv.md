## Overview

`kgtk import-csv` converts a CSV file in the KGTK node file format to a KGTK edge file. The input file need not contain an ID column, it can be added using `--add-id` optioin.

## Usage

```
usage: import-csv [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                  [-c COLUMNS [COLUMNS ...]] [--labels LABELS [LABELS ...]]
                  [--id-column ID_COLUMN_NAME] [-v [optional True|False]]
                  [--add-id ADD_ID] [--old-id-column-name COLUMN_NAME]
                  [--new-id-column-name COLUMN_NAME]
                  [--overwrite-id [optional true|false]]
                  [--verify-id-unique [optional true|false]]
                  [--id-style {compact-prefix,empty,node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,prefix###,wikidata,wikidata-with-claim-id}]
                  [--id-prefix PREFIX] [--initial-id INTEGER]
                  [--id-prefix-num-width INTEGER]
                  [--id-concat-num-width INTEGER]
                  [--value-hash-width VALUE_HASH_WIDTH]
                  [--claim-id-hash-width CLAIM_ID_HASH_WIDTH]
                  [--claim-id-column-name CLAIM_ID_COLUMN_NAME]
                  [--id-separator ID_SEPARATOR]

If called as "kgtk normalize-nodes", Normalize a KGTK node file into a KGTK edge file with a row for each column value in the input file.
If called as "kgtk import-csv", the input file is assumed to be a CSV file.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  -c COLUMNS [COLUMNS ...], --columns COLUMNS [COLUMNS ...]
                        Columns to remove as a space-separated list.
                        (default=all columns except id)
  --labels LABELS [LABELS ...]
                        Label names to use as a space-separated list.
                        (default=column names)
  --id-column ID_COLUMN_NAME
                        The name of the ID column. (default=id or alias)
  --add-id ADD_ID       Add an id column to the output. (default=False)
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
  --id-style {compact-prefix,empty,node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,prefix###,wikidata,wikidata-with-claim-id}
                        The ID generation style. (default=prefix###).
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

### Cities

Suppose we have the following table in `cities.csv`:

|name             |country             |subcountry        |geonameid|
|-----------------|--------------------|------------------|---------|
|les Escaldes     |Andorra             |Escaldes-Engordany|3040051  |
|Andorra la Vella |Andorra             |Andorra la Vella  |3041563  |
|Umm al Qaywayn   |United Arab Emirates|Umm al Qaywayn    |290594   |
|Ras al-Khaimah   |United Arab Emirates|Raʼs al Khaymah   |291074   |
|Khawr Fakkān     |United Arab Emirates|Ash Shāriqah      |291696   |
|Dubai            |United Arab Emirates|Dubai             |292223   |
|Dibba Al-Fujairah|United Arab Emirates|Al Fujayrah       |292231   |
|Dibba Al-Hisn    |United Arab Emirates|Al Fujayrah       |292239   |
|Sharjah          |United Arab Emirates|Ash Shāriqah      |292672   |
|...              |...                 |...               |...      |

Since we already have the `geonameid` column, we can use it as the ID column and convert the table to a KGTK edge file using the following command:

```bash
!kgtk import-csv \
    --id-column geonameid \
    --input-file ../../tests/data/cities.csv \
    --output-file normalized_cities.tsv
```

|node1  |label     |node2               |
|-------|----------|--------------------|
|3040051|name      |les Escaldes        |
|3040051|country   |Andorra             |
|3040051|subcountry|Escaldes-Engordany  |
|3041563|name      |Andorra la Vella    |
|3041563|country   |Andorra             |
|3041563|subcountry|Andorra la Vella    |
|290594 |name      |Umm al Qaywayn      |
|290594 |country   |United Arab Emirates|
|290594 |subcountry|Umm al Qaywayn      |
|291074 |name      |Ras al-Khaimah      |
|...    |...       |...                 |


### Paintings

Suppose we have the following table in `paintings.csv`:

|Painting                   |Artist               |Year of Painting|Adjusted Price|Original Price|Date of Sale|Year of Sale|Seller                             |Buyer                                                    |Auction House|Image                                                                                                                                                                  |Painting Wikipedia Profile                              |Artist Wikipedia Profile                          |Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|---------------------------|---------------------|----------------|--------------|--------------|------------|------------|-----------------------------------|---------------------------------------------------------|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|A Wheatfield with Cypresses|Vincent van Gogh     |1889            |$93,700,000   |$57,000,000   |1/05/1993   |1993        |Son of Emil Georg Bührle           |Walter H. Annenberg                                      |Private sale |http://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Vincent_Willem_van_Gogh_049.jpg/95px-Vincent_Willem_van_Gogh_049.jpg                                          |http://en.wikipedia.org/wiki/A_Wheatfield_with_Cypresses|http://en.wikipedia.org/wiki/Vincent_van_Gogh     |A Wheatfield with Cypresses (occasionally called A Cornfield with Cypresses) is any of three similar 1889 oil paintings by Vincent van Gogh, as part of his wheat field series. All were executed at the Saint-Paul-de-Mausole mental asylum at Saint-Rémy near Arles, France, where Van Gogh was voluntarily a patient from May 1889 to May 1890. The works were inspired by the view from the window at the asylum towards the Les Alpilles mountains.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|Acrobate et jeune arlequin |Pablo Picasso        |1905            |$75,900,000   |$38,500,000   |28/11/1988  |1988        |heir of Roger Janssen?             |Mitsukoshi                                               |Christie's   |http://uploads7.wikiart.org/images/pablo-picasso/acrobat-and-young-harlequin-1905.jpg                                                                                  |                                                        |                                                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|Adele Bloch-Bauer II       |Gustav Klimt         |1912            |$103,500,000  |$87,900,000   |2/11/2006   |2006        |Maria Altmann                      |                                                         |Christie's   |http://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Gustav_Klimt_047.jpg/95px-Gustav_Klimt_047.jpg                                                                |http://en.wikipedia.org/wiki/Adele_Bloch-Bauer_II       |                                                  |Adele Bloch-Bauer II is a 1912 painting by Gustav Klimt. Adele Bloch-Bauer was the wife of Ferdinand Bloch-Bauer, who was a wealthy industrialist who sponsored the arts and supported Gustav Klimt. Adele Bloch-Bauer was the only model to be painted twice by Klimt; she also appeared in the much more famous Portrait of Adele Bloch-Bauer I. Adele's portraits had hung in the family home prior to their seizure by the Nazis during WWII. The Austrian museum where they resided after the war was reluctant to return them to their rightful owners, hence a protracted court battle in the United States and in Austria (see Republic of Austria v. Altmann) ensued, which resulted in five Gustav Klimt paintings being returned to Maria Altmann, the niece of Ferdinand Bloch-Bauer, in January 2006. In November 2006, Christie's auction house sold Portrait of Adele Bloch-Bauer II at auction for almost $88 million, the fourth-highest priced piece of art at auction at the time.|
|Anna's Light               |Barnett Newman       |1968            |$107,300,000  |$105,700,000  |4/10/2013   |2013        |DIC Corp.                          |                                                         |Private sale |http://artpaintingartist.org/wp-content/uploads/2014/02/Annas-Light-by-Barnett-Newman.jpg                                                                              |                                                        |http://en.wikipedia.org/wiki/Barnett_Newman       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|Au Lapin Agile             |Pablo Picasso        |1904            |$76,600,000   |$40,700,000   |27/11/1989  |1989        |daughter of Joan Whitney Payson    |Walter H. Annenberg                                      |Sotheby's    |http://vineartshouston.files.wordpress.com/2012/05/picasso.jpg                                                                                                         |                                                        |                                                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|Bal du moulin de la Galette|Pierre-Auguste Renoir|1876            |$143,300,000  |$78,100,000   |17/05/1990  |1990        |Betsey Whitney                     |Ryoei Saito                                              |Sotheby's    |http://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Pierre-Auguste_Renoir%2C_Le_Moulin_de_la_Galette.jpg/95px-Pierre-Auguste_Renoir%2C_Le_Moulin_de_la_Galette.jpg|http://en.wikipedia.org/wiki/Bal_du_moulin_de_la_Galette|http://en.wikipedia.org/wiki/Pierre-Auguste_Renoir|Bal du moulin de la Galette (commonly known as Dance at Le moulin de la Galette) is an 1876 painting by French artist Pierre-Auguste Renoir. It is housed at the Musée d'Orsay in Paris and is one of Impressionisms most celebrated masterpieces. The painting depicts a typical Sunday afternoon at Moulin de la Galette in the district of Montmartre in Paris. In the late 19th century, working class Parisians would dress up and spend time there dancing, drinking, and eating galettes into the evening.:121-3                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|Black Fire I               |Barnett Newman       |1961            |$84,200,000   |$84,200,000   |13/05/2014  |2014        |Private Collection                 |Anonymous                                                |Christie's   |http://www.christies.com/media-library/images/salelandingpage/thumb/pwcmay2014/black-fire-index.jpg                                                                    |                                                        |http://en.wikipedia.org/wiki/Barnett_Newman       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|Darmstadt Madonna          |Hans Holbein         |1526            |$78,700,000   |$75,000,000   |12/07/2011  |2011        |Donatus, Hereditary Prince of Hesse|Reinhold Würth                                           |Private sale |http://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Darmstadtmadonna.jpg/95px-Darmstadtmadonna.jpg                                                                |http://en.wikipedia.org/wiki/Darmstadt_Madonna          |http://en.wikipedia.org/wiki/Hans_Holbein         |The Darmstadt Madonna (also known as the Madonna of Jakob Meyer zum Hasen) is an oil painting by Hans Holbein the Younger. Completed in 1526 in Basel, the work shows the Bürgermeister of Basel Jakob Meyer zum Hasen, his first wife (who had died earlier), his current wife, and his daughter grouped around the Madonna and infant Jesus. The meaning of the two other male figures on the left side is, like the overall iconography of the image, not entirely clear. The image testified to the resolutely Catholic faith of the Bürgermeister, who actively opposed the Reformation.                                                                                                                                                                                                                                                                                                                                                                                                        |
|Diana and Actaeon          |Titian               |1556, 1559      |$78,900,000   |$70,600,000   |1/02/2009   |2009        |Duke of Sutherland                 |National Galleries of Scotland & National Gallery, London|Private sale |http://www.nationalgallery.org.uk/upload/img/titian-diana-and-actaeon-NG6611-fm.jpg                                                                                    |http://en.wikipedia.org/wiki/Diana_and_Actaeon_(Titian) |                                                  |Diana and Actaeon is a painting by the Italian Renaissance master Titian, finished in 1556–1559, and is considered amongst Titian's greatest works. It portrays the moment in which the goddess Diana meets Actaeon. In 2008–2009, the National Gallery, London and National Gallery of Scotland successfully campaigned to acquire the painting from the Bridgewater Collection for £50 million. As a result, Diana and Actaeon will remain on display in the UK, and will alternate between the two galleries on five-year terms.                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|...                        |...                  |...             |...           |...           |...         |...         |...                                |...                                                      |...          |...                                                                                                                                                                    |...                                                     |...                                               |...                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

Since we don't have an ID column, we can use the `--add-id` option to add an ID column to the output:

```bash
!kgtk import-csv \
    --add-id True \
    --input-file ../../tests/data/Paintings.csv \
    --output-file normalized_Paintings.tsv
```

|node1|label           |node2                      |
|-----|----------------|---------------------------|
|E1   |Painting        |A Wheatfield with Cypresses|
|E1   |Artist          |Vincent van Gogh           |
|E1   |Year of Painting|1889                       |
|E1   |Adjusted Price  |$93,700,000                |
|E1   |Original Price  |$57,000,000                |
|E1   |Date of Sale    |1/05/1993                  |
|E1   |Year of Sale    |1993                       |
|E1   |Seller          |Son of Emil Georg Bührle   |
|E1   |Buyer           |Walter H. Annenberg        |
|E1   |Auction House   |Private sale               |
|...  |...             |...                        |

### Calendar

Suppose we have the following table in `calendar.csv`:

|Bulan           |Nama_Event                                      |Nama_Sirkuit                          |Lat       |Long      |
|----------------|------------------------------------------------|--------------------------------------|----------|----------|
|14 November 2017|Valencia MotoGP™ Official Test                  |Circuit Ricardo Tormo SPAIN           |39.486863 |-0.629870 |
|28 January 2018 |Sepang MotoGP™ Official Test                    |Sepang International Circuit MALAYSIA |2.759414  |101.731778|
|16 February 2018|Buriram MotoGP™ Official Test                   |Buriram International Circuit THAILAND|14.957971 |103.084925|
|1 March 2018    |Qatar MotoGP™ Official Test                     |Losail International Circuit QATAR    |25.486109 |51.452779 |
|18 March 2018   |1 -  Grand Prix of Qatar                        |Losail International Circuit QATAR    |25.486109 |51.452779 |
|8 April 2018    |2 -  Gran Premio Motul de la República Argentina|Termas de Río Hondo ARGENTINA         |-27.498557|-64.860536|
|22 April 2018   |3 -  Red Bull Grand Prix of The Americas        |Circuit Of The Americas UNITED STATES |30.134581 |-97.635851|
|6 May 2018      |4 -  Gran Premio Red Bull de España             |Circuito de Jerez SPAIN               |36.709299 |-6.033878 |
|20 May 2018     |5 -  HJC Helmets Grand Prix de France           |Le Mans FRANCE                        |47.953730 |0.213367  |
|...             |...                                             |...                                   |...       |...       |

If this is a `;` seperated file, we can use the `--column-separator` option to specify the delimiter:

```bash
!kgtk import-csv \
    --column-separator ';' \
    --add-id True \
    --input-file ../../tests/data/Calendar_2018_geopoint.csv \
    --output-file normalized_Calendar_2018_geopoint.tsv
```

|node1|label       |node2                                |
|-----|------------|-------------------------------------|
|E1   |Bulan       |14 November 2017                     |
|E1   |Nama_Event  |Valencia MotoGP™ Official Test       |
|E1   |Nama_Sirkuit|Circuit Ricardo Tormo SPAIN          |
|E1   |Lat         |39.486863                            |
|E1   |Long        |-0.629870                            |
|E2   |Bulan       |28 January 2018                      |
|E2   |Nama_Event  |Sepang MotoGP™ Official Test         |
|E2   |Nama_Sirkuit|Sepang International Circuit MALAYSIA|
|E2   |Lat         |2.759414                             |
|E2   |Long        |101.731778                           |
|...  |...         |...                                  |
