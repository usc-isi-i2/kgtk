## Overview

`kgtk normalize-nodes` converts a KGTK node file to a KGTK edge file.

### Relationship Names

By default, the input file's column headers are used as relationship
names in the output file's `label` column.  The `--labels` option can be used to provide
a different set of relationship names in the output file.

## Usage

```
usage: kgtk normalize-nodes [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                            [-c COLUMNS [COLUMNS ...]]
                            [--labels LABELS [LABELS ...]]
                            [--id-column ID_COLUMN_NAME]
                            [-v [optional True|False]]

Normalize a KGTK node file into a KGTK edge file with a row for each column value in the input file.

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

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Sample Data: The First 18 Elements

Here is a file containing some physical properties and categories for the
first 18 elements in the Period Table of Elements and Properties.

```bash
kgtk cat -i examples/docs/periodic_table_of_elements_1-18.tsv
```

| id | AtomicNumber | Element | Symbol | AtomicMass | NumberofNeutrons | NumberofProtons | NumberofElectrons | Period | Group | Phase | Radioactive | Natural | Metal | Nonmetal | Metalloid | Type | AtomicRadius | Electronegativity | FirstIonization | Density | MeltingPoint | BoilingPoint | NumberOfIsotopes | Discoverer | Year | SpecificHeat | NumberofShells | NumberofValence |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| H | 1 | Hydrogen | H | 1.007 | 0 | 1 | 1 | 1 | 1 | gas |  | yes |  | yes |  | Nonmetal | 0.79 | 2.2 | 13.5984 | 8.99E-05 | 14.175 | 20.28 | 3 | Cavendish | 1766 | 14.304 | 1 | 1 |
| He | 2 | Helium | He | 4.002 | 2 | 2 | 2 | 1 | 18 | gas |  | yes |  | yes |  | NobleGas | 0.49 |  | 24.5874 | 1.79E-04 |  | 4.22 | 5 | Janssen | 1868 | 5.193 | 1 |  |
| Li | 3 | Lithium | Li | 6.941 | 4 | 3 | 3 | 2 | 1 | solid |  | yes | yes |  |  | AlkaliMetal | 2.1 | 0.98 | 5.3917 | 5.34E-01 | 453.85 | 1615 | 5 | Arfvedson | 1817 | 3.582 | 2 | 1 |
| Be | 4 | Beryllium | Be | 9.012 | 5 | 4 | 4 | 2 | 2 | solid |  | yes | yes |  |  | AlkalineEarthMetal | 1.4 | 1.57 | 9.3227 | 1.85E+00 | 1560.15 | 2742 | 6 | Vaulquelin | 1798 | 1.825 | 2 | 2 |
| B | 5 | Boron | B | 10.811 | 6 | 5 | 5 | 2 | 13 | solid |  | yes |  |  | yes | Metalloid | 1.2 | 2.04 | 8.298 | 2.34E+00 | 2573.15 | 4200 | 6 | Gay-Lussac | 1808 | 1.026 | 2 | 3 |
| C | 6 | Carbon | C | 12.011 | 6 | 6 | 6 | 2 | 14 | solid |  | yes |  | yes |  | Nonmetal | 0.91 | 2.55 | 11.2603 | 2.27E+00 | 3948.15 | 4300 | 7 | Prehistoric |  | 0.709 | 2 | 4 |
| N | 7 | Nitrogen | N | 14.007 | 7 | 7 | 7 | 2 | 15 | gas |  | yes |  | yes |  | Nonmetal | 0.75 | 3.04 | 14.5341 | 1.25E-03 | 63.29 | 77.36 | 8 | Rutherford | 1772 | 1.04 | 2 | 5 |
| O | 8 | Oxygen | O | 15.999 | 8 | 8 | 8 | 2 | 16 | gas |  | yes |  | yes |  | Nonmetal | 0.65 | 3.44 | 13.6181 | 1.43E-03 | 50.5 | 90.2 | 8 | Priestley\|Scheele | 1774 | 0.918 | 2 | 6 |
| F | 9 | Fluorine | F | 18.998 | 10 | 9 | 9 | 2 | 17 | gas |  | yes |  | yes |  | Halogen | 0.57 | 3.98 | 17.4228 | 1.70E-03 | 53.63 | 85.03 | 6 | Moissan | 1886 | 0.824 | 2 | 7 |
| Ne | 10 | Neon | Ne | 20.18 | 10 | 10 | 10 | 2 | 18 | gas |  | yes |  | yes |  | Noble Gas | 0.51 |  | 21.5645 | 9.00E-04 | 24.703 | 27.07 | 8 | Ramsay_and_Travers | 1898 | 1.03 | 2 | 8 |
| Na | 11 | Sodium | Na | 22.99 | 12 | 11 | 11 | 3 | 1 | solid |  | yes | yes |  |  | AlkaliMetal | 2.2 | 0.93 | 5.1391 | 9.71E-01 | 371.15 | 1156 | 7 | Davy | 1807 | 1.228 | 3 | 1 |
| Mg | 12 | Magnesium | Mg | 24.305 | 12 | 12 | 12 | 3 | 2 | solid |  | yes | yes |  |  | AlkalineEarthMetal | 1.7 | 1.31 | 7.6462 | 1.74E+00 | 923.15 | 1363 | 8 | Black | 1755 | 1.023 | 3 | 2 |
| Al | 13 | Aluminum | Al | 26.982 | 14 | 13 | 13 | 3 | 13 | solid |  | yes | yes |  |  | Metal | 1.8 | 1.61 | 5.9858 | 2.70E+00 | 933.4 | 2792 | 8 | Wshler | 1827 | 0.897 | 3 | 3 |
| Si | 14 | Silicon | Si | 28.086 | 14 | 14 | 14 | 3 | 14 | solid |  | yes |  |  | yes | Metalloid | 1.5 | 1.9 | 8.1517 | 2.33E+00 | 1683.15 | 3538 | 8 | Berzelius | 1824 | 0.705 | 3 | 4 |
| P | 15 | Phosphorus | P | 30.974 | 16 | 15 | 15 | 3 | 15 | solid |  | yes |  | yes |  | Nonmetal | 1.2 | 2.19 | 10.4867 | 1.82E+00 | 317.25 | 553 | 7 | BranBrand | 1669 | 0.769 | 3 | 5 |
| S | 16 | Sulfur | S | 32.065 | 16 | 16 | 16 | 3 | 16 | solid |  | yes |  | yes |  | Nonmetal | 1.1 | 2.58 | 10.36 | 2.07E+00 | 388.51 | 717.8 | 10 | Prehistoric |  | 0.71 | 3 | 6 |
| Cl | 17 | Chlorine | Cl | 35.453 | 18 | 17 | 17 | 3 | 17 | gas |  | yes |  | yes |  | Halogen | 0.97 | 3.16 | 12.9676 | 3.21E-03 | 172.31 | 239.11 | 11 | Scheele | 1774 | 0.479 | 3 | 7 |
| Ar | 18 | Argon | Ar | 39.948 | 22 | 18 | 18 | 3 | 18 | gas |  | yes |  | yes |  | NobleGas | 0.88 |  | 15.7596 | 1.78E-03 | 83.96 | 87.3 | 8 | Rayleigh_and_Ramsay | 1894 | 0.52 | 3 | 8 |

### Default Conversion

```bash
kgtk normalize-nodes -i examples/docs/periodic_table_of_elements_1-18.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| H | AtomicNumber | 1 |
| H | Element | Hydrogen |
| H | Symbol | H |
| H | AtomicMass | 1.007 |
| H | NumberofNeutrons | 0 |
| H | NumberofProtons | 1 |
| H | NumberofElectrons | 1 |
| H | Period | 1 |
| H | Group | 1 |
| H | Phase | gas |
| H | Natural | yes |
| H | Nonmetal | yes |
| H | Type | Nonmetal |
| H | AtomicRadius | 0.79 |
| H | Electronegativity | 2.2 |
| H | FirstIonization | 13.5984 |
| H | Density | 8.99E-05 |
| H | MeltingPoint | 14.175 |
| H | BoilingPoint | 20.28 |
| H | NumberOfIsotopes | 3 |
| H | Discoverer | Cavendish |
| H | Year | 1766 |
| H | SpecificHeat | 14.304 |
| H | NumberofShells | 1 |
| H | NumberofValence | 1 |
| He | AtomicNumber | 2 |
| He | Element | Helium |
| He | Symbol | He |
| He | AtomicMass | 4.002 |
| He | NumberofNeutrons | 2 |
| He | NumberofProtons | 2 |
| He | NumberofElectrons | 2 |
| He | Period | 1 |
| He | Group | 18 |
| He | Phase | gas |
| He | Natural | yes |
| He | Nonmetal | yes |
| He | Type | NobleGas |
| He | AtomicRadius | 0.49 |
| He | FirstIonization | 24.5874 |
| He | Density | 1.79E-04 |
| He | BoilingPoint | 4.22 |
| He | NumberOfIsotopes | 5 |
| He | Discoverer | Janssen |
| He | Year | 1868 |
| He | SpecificHeat | 5.193 |
| He | NumberofShells | 1 |
| Li | AtomicNumber | 3 |
| Li | Element | Lithium |
| Li | Symbol | Li |
| Li | AtomicMass | 6.941 |
| Li | NumberofNeutrons | 4 |
| Li | NumberofProtons | 3 |
| Li | NumberofElectrons | 3 |
| Li | Period | 2 |
| Li | Group | 1 |
| Li | Phase | solid |
| Li | Natural | yes |
| Li | Metal | yes |
| Li | Type | AlkaliMetal |
| Li | AtomicRadius | 2.1 |
| Li | Electronegativity | 0.98 |
| Li | FirstIonization | 5.3917 |
| Li | Density | 5.34E-01 |
| Li | MeltingPoint | 453.85 |
| Li | BoilingPoint | 1615 |
| Li | NumberOfIsotopes | 5 |
| Li | Discoverer | Arfvedson |
| Li | Year | 1817 |
| Li | SpecificHeat | 3.582 |
| Li | NumberofShells | 2 |
| Li | NumberofValence | 1 |
| Be | AtomicNumber | 4 |
| Be | Element | Beryllium |
| Be | Symbol | Be |
| Be | AtomicMass | 9.012 |
| Be | NumberofNeutrons | 5 |
| Be | NumberofProtons | 4 |
| Be | NumberofElectrons | 4 |
| Be | Period | 2 |
| Be | Group | 2 |
| Be | Phase | solid |
| Be | Natural | yes |
| Be | Metal | yes |
| Be | Type | AlkalineEarthMetal |
| Be | AtomicRadius | 1.4 |
| Be | Electronegativity | 1.57 |
| Be | FirstIonization | 9.3227 |
| Be | Density | 1.85E+00 |
| Be | MeltingPoint | 1560.15 |
| Be | BoilingPoint | 2742 |
| Be | NumberOfIsotopes | 6 |
| Be | Discoverer | Vaulquelin |
| Be | Year | 1798 |
| Be | SpecificHeat | 1.825 |
| Be | NumberofShells | 2 |
| Be | NumberofValence | 2 |
| B | AtomicNumber | 5 |
| B | Element | Boron |
| B | Symbol | B |
| B | AtomicMass | 10.811 |
| B | NumberofNeutrons | 6 |
| B | NumberofProtons | 5 |
| B | NumberofElectrons | 5 |
| B | Period | 2 |
| B | Group | 13 |
| B | Phase | solid |
| B | Natural | yes |
| B | Metalloid | yes |
| B | Type | Metalloid |
| B | AtomicRadius | 1.2 |
| B | Electronegativity | 2.04 |
| B | FirstIonization | 8.298 |
| B | Density | 2.34E+00 |
| B | MeltingPoint | 2573.15 |
| B | BoilingPoint | 4200 |
| B | NumberOfIsotopes | 6 |
| B | Discoverer | Gay-Lussac |
| B | Year | 1808 |
| B | SpecificHeat | 1.026 |
| B | NumberofShells | 2 |
| B | NumberofValence | 3 |
| C | AtomicNumber | 6 |
| C | Element | Carbon |
| C | Symbol | C |
| C | AtomicMass | 12.011 |
| C | NumberofNeutrons | 6 |
| C | NumberofProtons | 6 |
| C | NumberofElectrons | 6 |
| C | Period | 2 |
| C | Group | 14 |
| C | Phase | solid |
| C | Natural | yes |
| C | Nonmetal | yes |
| C | Type | Nonmetal |
| C | AtomicRadius | 0.91 |
| C | Electronegativity | 2.55 |
| C | FirstIonization | 11.2603 |
| C | Density | 2.27E+00 |
| C | MeltingPoint | 3948.15 |
| C | BoilingPoint | 4300 |
| C | NumberOfIsotopes | 7 |
| C | Discoverer | Prehistoric |
| C | SpecificHeat | 0.709 |
| C | NumberofShells | 2 |
| C | NumberofValence | 4 |
| N | AtomicNumber | 7 |
| N | Element | Nitrogen |
| N | Symbol | N |
| N | AtomicMass | 14.007 |
| N | NumberofNeutrons | 7 |
| N | NumberofProtons | 7 |
| N | NumberofElectrons | 7 |
| N | Period | 2 |
| N | Group | 15 |
| N | Phase | gas |
| N | Natural | yes |
| N | Nonmetal | yes |
| N | Type | Nonmetal |
| N | AtomicRadius | 0.75 |
| N | Electronegativity | 3.04 |
| N | FirstIonization | 14.5341 |
| N | Density | 1.25E-03 |
| N | MeltingPoint | 63.29 |
| N | BoilingPoint | 77.36 |
| N | NumberOfIsotopes | 8 |
| N | Discoverer | Rutherford |
| N | Year | 1772 |
| N | SpecificHeat | 1.04 |
| N | NumberofShells | 2 |
| N | NumberofValence | 5 |
| O | AtomicNumber | 8 |
| O | Element | Oxygen |
| O | Symbol | O |
| O | AtomicMass | 15.999 |
| O | NumberofNeutrons | 8 |
| O | NumberofProtons | 8 |
| O | NumberofElectrons | 8 |
| O | Period | 2 |
| O | Group | 16 |
| O | Phase | gas |
| O | Natural | yes |
| O | Nonmetal | yes |
| O | Type | Nonmetal |
| O | AtomicRadius | 0.65 |
| O | Electronegativity | 3.44 |
| O | FirstIonization | 13.6181 |
| O | Density | 1.43E-03 |
| O | MeltingPoint | 50.5 |
| O | BoilingPoint | 90.2 |
| O | NumberOfIsotopes | 8 |
| O | Discoverer | Priestley |
| O | Discoverer | Scheele |
| O | Year | 1774 |
| O | SpecificHeat | 0.918 |
| O | NumberofShells | 2 |
| O | NumberofValence | 6 |
| F | AtomicNumber | 9 |
| F | Element | Fluorine |
| F | Symbol | F |
| F | AtomicMass | 18.998 |
| F | NumberofNeutrons | 10 |
| F | NumberofProtons | 9 |
| F | NumberofElectrons | 9 |
| F | Period | 2 |
| F | Group | 17 |
| F | Phase | gas |
| F | Natural | yes |
| F | Nonmetal | yes |
| F | Type | Halogen |
| F | AtomicRadius | 0.57 |
| F | Electronegativity | 3.98 |
| F | FirstIonization | 17.4228 |
| F | Density | 1.70E-03 |
| F | MeltingPoint | 53.63 |
| F | BoilingPoint | 85.03 |
| F | NumberOfIsotopes | 6 |
| F | Discoverer | Moissan |
| F | Year | 1886 |
| F | SpecificHeat | 0.824 |
| F | NumberofShells | 2 |
| F | NumberofValence | 7 |
| Ne | AtomicNumber | 10 |
| Ne | Element | Neon |
| Ne | Symbol | Ne |
| Ne | AtomicMass | 20.18 |
| Ne | NumberofNeutrons | 10 |
| Ne | NumberofProtons | 10 |
| Ne | NumberofElectrons | 10 |
| Ne | Period | 2 |
| Ne | Group | 18 |
| Ne | Phase | gas |
| Ne | Natural | yes |
| Ne | Nonmetal | yes |
| Ne | Type | Noble Gas |
| Ne | AtomicRadius | 0.51 |
| Ne | FirstIonization | 21.5645 |
| Ne | Density | 9.00E-04 |
| Ne | MeltingPoint | 24.703 |
| Ne | BoilingPoint | 27.07 |
| Ne | NumberOfIsotopes | 8 |
| Ne | Discoverer | Ramsay_and_Travers |
| Ne | Year | 1898 |
| Ne | SpecificHeat | 1.03 |
| Ne | NumberofShells | 2 |
| Ne | NumberofValence | 8 |
| Na | AtomicNumber | 11 |
| Na | Element | Sodium |
| Na | Symbol | Na |
| Na | AtomicMass | 22.99 |
| Na | NumberofNeutrons | 12 |
| Na | NumberofProtons | 11 |
| Na | NumberofElectrons | 11 |
| Na | Period | 3 |
| Na | Group | 1 |
| Na | Phase | solid |
| Na | Natural | yes |
| Na | Metal | yes |
| Na | Type | AlkaliMetal |
| Na | AtomicRadius | 2.2 |
| Na | Electronegativity | 0.93 |
| Na | FirstIonization | 5.1391 |
| Na | Density | 9.71E-01 |
| Na | MeltingPoint | 371.15 |
| Na | BoilingPoint | 1156 |
| Na | NumberOfIsotopes | 7 |
| Na | Discoverer | Davy |
| Na | Year | 1807 |
| Na | SpecificHeat | 1.228 |
| Na | NumberofShells | 3 |
| Na | NumberofValence | 1 |
| Mg | AtomicNumber | 12 |
| Mg | Element | Magnesium |
| Mg | Symbol | Mg |
| Mg | AtomicMass | 24.305 |
| Mg | NumberofNeutrons | 12 |
| Mg | NumberofProtons | 12 |
| Mg | NumberofElectrons | 12 |
| Mg | Period | 3 |
| Mg | Group | 2 |
| Mg | Phase | solid |
| Mg | Natural | yes |
| Mg | Metal | yes |
| Mg | Type | AlkalineEarthMetal |
| Mg | AtomicRadius | 1.7 |
| Mg | Electronegativity | 1.31 |
| Mg | FirstIonization | 7.6462 |
| Mg | Density | 1.74E+00 |
| Mg | MeltingPoint | 923.15 |
| Mg | BoilingPoint | 1363 |
| Mg | NumberOfIsotopes | 8 |
| Mg | Discoverer | Black |
| Mg | Year | 1755 |
| Mg | SpecificHeat | 1.023 |
| Mg | NumberofShells | 3 |
| Mg | NumberofValence | 2 |
| Al | AtomicNumber | 13 |
| Al | Element | Aluminum |
| Al | Symbol | Al |
| Al | AtomicMass | 26.982 |
| Al | NumberofNeutrons | 14 |
| Al | NumberofProtons | 13 |
| Al | NumberofElectrons | 13 |
| Al | Period | 3 |
| Al | Group | 13 |
| Al | Phase | solid |
| Al | Natural | yes |
| Al | Metal | yes |
| Al | Type | Metal |
| Al | AtomicRadius | 1.8 |
| Al | Electronegativity | 1.61 |
| Al | FirstIonization | 5.9858 |
| Al | Density | 2.70E+00 |
| Al | MeltingPoint | 933.4 |
| Al | BoilingPoint | 2792 |
| Al | NumberOfIsotopes | 8 |
| Al | Discoverer | Wshler |
| Al | Year | 1827 |
| Al | SpecificHeat | 0.897 |
| Al | NumberofShells | 3 |
| Al | NumberofValence | 3 |
| Si | AtomicNumber | 14 |
| Si | Element | Silicon |
| Si | Symbol | Si |
| Si | AtomicMass | 28.086 |
| Si | NumberofNeutrons | 14 |
| Si | NumberofProtons | 14 |
| Si | NumberofElectrons | 14 |
| Si | Period | 3 |
| Si | Group | 14 |
| Si | Phase | solid |
| Si | Natural | yes |
| Si | Metalloid | yes |
| Si | Type | Metalloid |
| Si | AtomicRadius | 1.5 |
| Si | Electronegativity | 1.9 |
| Si | FirstIonization | 8.1517 |
| Si | Density | 2.33E+00 |
| Si | MeltingPoint | 1683.15 |
| Si | BoilingPoint | 3538 |
| Si | NumberOfIsotopes | 8 |
| Si | Discoverer | Berzelius |
| Si | Year | 1824 |
| Si | SpecificHeat | 0.705 |
| Si | NumberofShells | 3 |
| Si | NumberofValence | 4 |
| P | AtomicNumber | 15 |
| P | Element | Phosphorus |
| P | Symbol | P |
| P | AtomicMass | 30.974 |
| P | NumberofNeutrons | 16 |
| P | NumberofProtons | 15 |
| P | NumberofElectrons | 15 |
| P | Period | 3 |
| P | Group | 15 |
| P | Phase | solid |
| P | Natural | yes |
| P | Nonmetal | yes |
| P | Type | Nonmetal |
| P | AtomicRadius | 1.2 |
| P | Electronegativity | 2.19 |
| P | FirstIonization | 10.4867 |
| P | Density | 1.82E+00 |
| P | MeltingPoint | 317.25 |
| P | BoilingPoint | 553 |
| P | NumberOfIsotopes | 7 |
| P | Discoverer | BranBrand |
| P | Year | 1669 |
| P | SpecificHeat | 0.769 |
| P | NumberofShells | 3 |
| P | NumberofValence | 5 |
| S | AtomicNumber | 16 |
| S | Element | Sulfur |
| S | Symbol | S |
| S | AtomicMass | 32.065 |
| S | NumberofNeutrons | 16 |
| S | NumberofProtons | 16 |
| S | NumberofElectrons | 16 |
| S | Period | 3 |
| S | Group | 16 |
| S | Phase | solid |
| S | Natural | yes |
| S | Nonmetal | yes |
| S | Type | Nonmetal |
| S | AtomicRadius | 1.1 |
| S | Electronegativity | 2.58 |
| S | FirstIonization | 10.36 |
| S | Density | 2.07E+00 |
| S | MeltingPoint | 388.51 |
| S | BoilingPoint | 717.8 |
| S | NumberOfIsotopes | 10 |
| S | Discoverer | Prehistoric |
| S | SpecificHeat | 0.71 |
| S | NumberofShells | 3 |
| S | NumberofValence | 6 |
| Cl | AtomicNumber | 17 |
| Cl | Element | Chlorine |
| Cl | Symbol | Cl |
| Cl | AtomicMass | 35.453 |
| Cl | NumberofNeutrons | 18 |
| Cl | NumberofProtons | 17 |
| Cl | NumberofElectrons | 17 |
| Cl | Period | 3 |
| Cl | Group | 17 |
| Cl | Phase | gas |
| Cl | Natural | yes |
| Cl | Nonmetal | yes |
| Cl | Type | Halogen |
| Cl | AtomicRadius | 0.97 |
| Cl | Electronegativity | 3.16 |
| Cl | FirstIonization | 12.9676 |
| Cl | Density | 3.21E-03 |
| Cl | MeltingPoint | 172.31 |
| Cl | BoilingPoint | 239.11 |
| Cl | NumberOfIsotopes | 11 |
| Cl | Discoverer | Scheele |
| Cl | Year | 1774 |
| Cl | SpecificHeat | 0.479 |
| Cl | NumberofShells | 3 |
| Cl | NumberofValence | 7 |
| Ar | AtomicNumber | 18 |
| Ar | Element | Argon |
| Ar | Symbol | Ar |
| Ar | AtomicMass | 39.948 |
| Ar | NumberofNeutrons | 22 |
| Ar | NumberofProtons | 18 |
| Ar | NumberofElectrons | 18 |
| Ar | Period | 3 |
| Ar | Group | 18 |
| Ar | Phase | gas |
| Ar | Natural | yes |
| Ar | Nonmetal | yes |
| Ar | Type | NobleGas |
| Ar | AtomicRadius | 0.88 |
| Ar | FirstIonization | 15.7596 |
| Ar | Density | 1.78E-03 |
| Ar | MeltingPoint | 83.96 |
| Ar | BoilingPoint | 87.3 |
| Ar | NumberOfIsotopes | 8 |
| Ar | Discoverer | Rayleigh_and_Ramsay |
| Ar | Year | 1894 |
| Ar | SpecificHeat | 0.52 |
| Ar | NumberofShells | 3 |
| Ar | NumberofValence | 8 |

### Convert Specific Columns

```bash
kgtk normalize-nodes -i examples/docs/periodic_table_of_elements_1-18.tsv \
                     --columns AtomicNumber Element Symbol AtomicMass
```

| node1 | label | node2 |
| -- | -- | -- |
| H | AtomicNumber | 1 |
| H | Element | Hydrogen |
| H | Symbol | H |
| H | AtomicMass | 1.007 |
| He | AtomicNumber | 2 |
| He | Element | Helium |
| He | Symbol | He |
| He | AtomicMass | 4.002 |
| Li | AtomicNumber | 3 |
| Li | Element | Lithium |
| Li | Symbol | Li |
| Li | AtomicMass | 6.941 |
| Be | AtomicNumber | 4 |
| Be | Element | Beryllium |
| Be | Symbol | Be |
| Be | AtomicMass | 9.012 |
| B | AtomicNumber | 5 |
| B | Element | Boron |
| B | Symbol | B |
| B | AtomicMass | 10.811 |
| C | AtomicNumber | 6 |
| C | Element | Carbon |
| C | Symbol | C |
| C | AtomicMass | 12.011 |
| N | AtomicNumber | 7 |
| N | Element | Nitrogen |
| N | Symbol | N |
| N | AtomicMass | 14.007 |
| O | AtomicNumber | 8 |
| O | Element | Oxygen |
| O | Symbol | O |
| O | AtomicMass | 15.999 |
| F | AtomicNumber | 9 |
| F | Element | Fluorine |
| F | Symbol | F |
| F | AtomicMass | 18.998 |
| Ne | AtomicNumber | 10 |
| Ne | Element | Neon |
| Ne | Symbol | Ne |
| Ne | AtomicMass | 20.18 |
| Na | AtomicNumber | 11 |
| Na | Element | Sodium |
| Na | Symbol | Na |
| Na | AtomicMass | 22.99 |
| Mg | AtomicNumber | 12 |
| Mg | Element | Magnesium |
| Mg | Symbol | Mg |
| Mg | AtomicMass | 24.305 |
| Al | AtomicNumber | 13 |
| Al | Element | Aluminum |
| Al | Symbol | Al |
| Al | AtomicMass | 26.982 |
| Si | AtomicNumber | 14 |
| Si | Element | Silicon |
| Si | Symbol | Si |
| Si | AtomicMass | 28.086 |
| P | AtomicNumber | 15 |
| P | Element | Phosphorus |
| P | Symbol | P |
| P | AtomicMass | 30.974 |
| S | AtomicNumber | 16 |
| S | Element | Sulfur |
| S | Symbol | S |
| S | AtomicMass | 32.065 |
| Cl | AtomicNumber | 17 |
| Cl | Element | Chlorine |
| Cl | Symbol | Cl |
| Cl | AtomicMass | 35.453 |
| Ar | AtomicNumber | 18 |
| Ar | Element | Argon |
| Ar | Symbol | Ar |
| Ar | AtomicMass | 39.948 |

### Convert Specific Columns with Alternate Relationship Names

`--labels LABEL ...` allows you to specify the relationsip symbols used in the
output KGTK edge file.  When this option is specified, one lable must be
supplied for each column extracted.

```bash
kgtk normalize-nodes -i examples/docs/periodic_table_of_elements_1-18.tsv \
                     --columns AtomicNumber Element AtomicMass \
                     --labels atomic_number element atomic_mass
```

| node1 | label | node2 |
| -- | -- | -- |
| H | atomic_number | 1 |
| H | element | Hydrogen |
| H | atomic_mass | 1.007 |
| He | atomic_number | 2 |
| He | element | Helium |
| He | atomic_mass | 4.002 |
| Li | atomic_number | 3 |
| Li | element | Lithium |
| Li | atomic_mass | 6.941 |
| Be | atomic_number | 4 |
| Be | element | Beryllium |
| Be | atomic_mass | 9.012 |
| B | atomic_number | 5 |
| B | element | Boron |
| B | atomic_mass | 10.811 |
| C | atomic_number | 6 |
| C | element | Carbon |
| C | atomic_mass | 12.011 |
| N | atomic_number | 7 |
| N | element | Nitrogen |
| N | atomic_mass | 14.007 |
| O | atomic_number | 8 |
| O | element | Oxygen |
| O | atomic_mass | 15.999 |
| F | atomic_number | 9 |
| F | element | Fluorine |
| F | atomic_mass | 18.998 |
| Ne | atomic_number | 10 |
| Ne | element | Neon |
| Ne | atomic_mass | 20.18 |
| Na | atomic_number | 11 |
| Na | element | Sodium |
| Na | atomic_mass | 22.99 |
| Mg | atomic_number | 12 |
| Mg | element | Magnesium |
| Mg | atomic_mass | 24.305 |
| Al | atomic_number | 13 |
| Al | element | Aluminum |
| Al | atomic_mass | 26.982 |
| Si | atomic_number | 14 |
| Si | element | Silicon |
| Si | atomic_mass | 28.086 |
| P | atomic_number | 15 |
| P | element | Phosphorus |
| P | atomic_mass | 30.974 |
| S | atomic_number | 16 |
| S | element | Sulfur |
| S | atomic_mass | 32.065 |
| Cl | atomic_number | 17 |
| Cl | element | Chlorine |
| Cl | atomic_mass | 35.453 |
| Ar | atomic_number | 18 |
| Ar | element | Argon |
| Ar | atomic_mass | 39.948 |

### Using An Alternate ID

`--id-column ID_COLUMN_NAME` specifies a column to be used instead of
the normal `id` column for the source of the `node1` values in the output file.

```bash
kgtk normalize-nodes -i examples/docs/periodic_table_of_elements_1-18.tsv \
                     --columns AtomicNumber Symbol AtomicMass \
                     --labels atomic_number symbol atomic_mass \
                     --id-column Element
```

| node1 | label | node2 |
| -- | -- | -- |
| Hydrogen | atomic_number | 1 |
| Hydrogen | symbol | H |
| Hydrogen | atomic_mass | 1.007 |
| Helium | atomic_number | 2 |
| Helium | symbol | He |
| Helium | atomic_mass | 4.002 |
| Lithium | atomic_number | 3 |
| Lithium | symbol | Li |
| Lithium | atomic_mass | 6.941 |
| Beryllium | atomic_number | 4 |
| Beryllium | symbol | Be |
| Beryllium | atomic_mass | 9.012 |
| Boron | atomic_number | 5 |
| Boron | symbol | B |
| Boron | atomic_mass | 10.811 |
| Carbon | atomic_number | 6 |
| Carbon | symbol | C |
| Carbon | atomic_mass | 12.011 |
| Nitrogen | atomic_number | 7 |
| Nitrogen | symbol | N |
| Nitrogen | atomic_mass | 14.007 |
| Oxygen | atomic_number | 8 |
| Oxygen | symbol | O |
| Oxygen | atomic_mass | 15.999 |
| Fluorine | atomic_number | 9 |
| Fluorine | symbol | F |
| Fluorine | atomic_mass | 18.998 |
| Neon | atomic_number | 10 |
| Neon | symbol | Ne |
| Neon | atomic_mass | 20.18 |
| Sodium | atomic_number | 11 |
| Sodium | symbol | Na |
| Sodium | atomic_mass | 22.99 |
| Magnesium | atomic_number | 12 |
| Magnesium | symbol | Mg |
| Magnesium | atomic_mass | 24.305 |
| Aluminum | atomic_number | 13 |
| Aluminum | symbol | Al |
| Aluminum | atomic_mass | 26.982 |
| Silicon | atomic_number | 14 |
| Silicon | symbol | Si |
| Silicon | atomic_mass | 28.086 |
| Phosphorus | atomic_number | 15 |
| Phosphorus | symbol | P |
| Phosphorus | atomic_mass | 30.974 |
| Sulfur | atomic_number | 16 |
| Sulfur | symbol | S |
| Sulfur | atomic_mass | 32.065 |
| Chlorine | atomic_number | 17 |
| Chlorine | symbol | Cl |
| Chlorine | atomic_mass | 35.453 |
| Argon | atomic_number | 18 |
| Argon | symbol | Ar |
| Argon | atomic_mass | 39.948 |

!!! note
    This example assumes that the input files contains an `id` field, but
    another field is being substituted for it.  If the input file does not
    contain an `id` field at all, the expert option `--mode=NONE` is also needed.

### Expert Example: CSV Input File without `id` Field

If the input file does not have an `id` field, the option `--id-column ID_COLUMN_NAME` may
be used to select a substitute for the `id` column.  The expert option `--mode=NONE`
is also needed.  This example also illustrates using a CSV file as an input file,
using the expert option `--input-format csv`.

```bash
kgtk normalize-nodes -i examples/docs/periodic_table_of_elements_1-18.csv \
                     --mode=NONE --input-format csv \
                     --columns AtomicNumber Symbol AtomicMass \
                     --labels atomic_number symbol atomic_mass \
                     --id-column Element
```

| node1 | label | node2 |
| -- | -- | -- |
| Hydrogen | atomic_number | 1 |
| Hydrogen | symbol | H |
| Hydrogen | atomic_mass | 1.007 |
| Helium | atomic_number | 2 |
| Helium | symbol | He |
| Helium | atomic_mass | 4.002 |
| Lithium | atomic_number | 3 |
| Lithium | symbol | Li |
| Lithium | atomic_mass | 6.941 |
| Beryllium | atomic_number | 4 |
| Beryllium | symbol | Be |
| Beryllium | atomic_mass | 9.012 |
| Boron | atomic_number | 5 |
| Boron | symbol | B |
| Boron | atomic_mass | 10.811 |
| Carbon | atomic_number | 6 |
| Carbon | symbol | C |
| Carbon | atomic_mass | 12.011 |
| Nitrogen | atomic_number | 7 |
| Nitrogen | symbol | N |
| Nitrogen | atomic_mass | 14.007 |
| Oxygen | atomic_number | 8 |
| Oxygen | symbol | O |
| Oxygen | atomic_mass | 15.999 |
| Fluorine | atomic_number | 9 |
| Fluorine | symbol | F |
| Fluorine | atomic_mass | 18.998 |
| Neon | atomic_number | 10 |
| Neon | symbol | Ne |
| Neon | atomic_mass | 20.18 |
| Sodium | atomic_number | 11 |
| Sodium | symbol | Na |
| Sodium | atomic_mass | 22.99 |
| Magnesium | atomic_number | 12 |
| Magnesium | symbol | Mg |
| Magnesium | atomic_mass | 24.305 |
| Aluminum | atomic_number | 13 |
| Aluminum | symbol | Al |
| Aluminum | atomic_mass | 26.982 |
| Silicon | atomic_number | 14 |
| Silicon | symbol | Si |
| Silicon | atomic_mass | 28.086 |
| Phosphorus | atomic_number | 15 |
| Phosphorus | symbol | P |
| Phosphorus | atomic_mass | 30.974 |
| Sulfur | atomic_number | 16 |
| Sulfur | symbol | S |
| Sulfur | atomic_mass | 32.065 |
| Chlorine | atomic_number | 17 |
| Chlorine | symbol | Cl |
| Chlorine | atomic_mass | 35.453 |
| Argon | atomic_number | 18 |
| Argon | symbol | Ar |
| Argon | atomic_mass | 39.948 |
