# Taxonomy Updates for the MVZ
The goal of this project is to compare the records from the Cal Poly Humboldt Museum of Vertibrate Zoology with the most updated taxonomy to find if any of their records are out of date.

We use information from the [Mammal Diversity Database](https://www.mammaldiversity.org/explore.html) to get the current accepted mammal taxonomy

## Data Conversion
First we need to convert the data gathered from the taxonomy database into a tree format so we can easily reference against it.

```
python .\convert_data.py --help
usage: convert_data.py [-h] [-i IN_FILE] [-o OUT_FILE]

Converts taxonomy data gathered from mammaldiversity.org into a nested json object file

optional arguments:
  -h, --help            show this help message and exit
  -i IN_FILE, --in_file IN_FILE
  -o OUT_FILE, --out_file OUT_FILE
```

### Input File Format
The records file must be of a utf-8 csv with fields "order", "family", "genus", and "specificEpithet"

### Example
```
python .\convert_data.py -i "./mdd/MDD_v1.10_6615species.csv" -o "taxonomy_tree.json"
```

## Data Comparison
Compare data from the museum collection with the accepted taxonomy tree found in the data conversion step

```
python .\compare_data.py --help
usage: compare_data.py [-h] [-tf TAXONOMY_FILE] [-rf RECORDS_FILE] [-or OUT_DIFF_RECORDS] [-oc OUT_DIFF_TAXA]

Compares museum taxonomy data with the current accepted taxonomy

optional arguments:
  -h, --help            show this help message and exit
  -tf TAXONOMY_FILE, --taxonomy_file TAXONOMY_FILE
  -rf RECORDS_FILE, --records_file RECORDS_FILE
  -or OUT_DIFF_RECORDS, --out_diff_records OUT_DIFF_RECORDS
  -oc OUT_DIFF_TAXA, --out_diff_taxa OUT_DIFF_TAXA
```

### Records File Format
The records file must be of a utf-8 csv with fields "Order", "Family", "Genus", and "Species"

### Example
```
python .\compare_data.py -tf "./out/taxonomy_tree.json" -rf "./mvz/mvz_data.csv" -or "./out/diff_records.csv" -oc "./out/diff_taxa.json"
```

## Contributors
Jacob Oakman
Ezra Alberts
