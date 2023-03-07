import argparse
import csv
import json

def convert_data(species_data):
    """Convert the taxonomy data from a csv format to a nested dictionary"""
    taxonomy_tree = {}
    for row in species_data:
        if row["order"] not in taxonomy_tree:
            taxonomy_tree[row["order"]] = {
                row["family"]: {
                    row["genus"]: {
                        row["specificEpithet"]: {}
                    }
                }
            }
        elif row["family"] not in taxonomy_tree[row["order"]]:
            taxonomy_tree[row["order"]][row["family"]] = {
                row["genus"]: {
                    row["specificEpithet"]: {}
                }
            }
        elif row["genus"] not in taxonomy_tree[row["order"]][row["family"]]:
            taxonomy_tree[row["order"]][row["family"]][row["genus"]] = {
                row["specificEpithet"]: {}
            }
        elif row["specificEpithet"] not in taxonomy_tree[row["order"]][row["family"]][row["genus"]]:
            taxonomy_tree[row["order"]][row["family"]][row["genus"]][row["specificEpithet"]] = {}
    return taxonomy_tree

def main():
    """Converts taxonomy data gathered from mammaldiversity.org into a nested json object file"""
    parser = parser = argparse.ArgumentParser(
                prog = 'convert_data.py',
                description = 'Converts taxonomy data gathered from mammaldiversity.org into a nested json object file',
                epilog = 'Written as a collaboration between Jacob and Ezra')
    
    parser.add_argument("-i", "--in_file", type=argparse.FileType('r', encoding="utf-8"), default="./mdd/MDD_v1.10_6615species.csv")
    parser.add_argument("-o", "--out_file", type=argparse.FileType('w', encoding="utf-8"), default="./out/taxonomy_tree.json")

    args = parser.parse_args()

    species_reader = csv.DictReader(args.in_file, delimiter=",")

    taxonomy_tree = convert_data(species_reader)

    json.dump(taxonomy_tree, args.out_file, indent=4)

if __name__ == "__main__":
    main()