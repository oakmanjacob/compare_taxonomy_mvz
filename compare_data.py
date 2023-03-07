
import argparse
import csv
import json

def check_for_divergance(tree, changes, name, next_name=""):
    """Checks whether a specific name appears at that level of the reference taxonomy and records changes"""

    if name not in tree:
        if next_name != "":
            found = False
            for new_name, next_names in tree.items():
                if next_name != "" and next_name in next_names:
                    found = True
                    if name not in changes:
                        changes[name] = [new_name]
                    elif new_name not in changes[name]:
                        changes[name].append(new_name)

            if not found and next_name != "" and name not in changes:
                changes[name] = []
        elif name not in changes:
            changes[name] = []
        return True
    return False

def compare_data(taxonomy_tree, museum_data):
    """Compares museum data vs the accepted current taxonomy and returns discrepancies"""
    unmatched_data = []
    changes = {
        "Order": {},
        "Family": {},
        "Genus": {},
        "Species": {},
    }

    for specimen in museum_data:
        order = specimen["Order"].strip().upper()
        family = specimen["Family"].strip().upper()
        genus = specimen["Genus"].strip()
        species = specimen["Species"].strip()

        specimen["NewOrder"] = ""
        specimen["NewFamily"] = ""
        specimen["NewGenus"] = ""

        if order == "" or family == "" or genus == "" or species == "":
            continue

        if check_for_divergance(taxonomy_tree, changes["Order"], order, family):
            specimen["NewOrder"] = "|".join(changes["Order"][order])
            unmatched_data.append(specimen)
            continue

        if check_for_divergance(taxonomy_tree[order], changes["Family"], family, genus):
            specimen["NewFamily"] = "|".join(changes["Family"][family])
            unmatched_data.append(specimen)
            continue

        if check_for_divergance(taxonomy_tree[order][family], changes["Genus"], genus, species):
            specimen["NewGenus"] = "|".join(changes["Genus"][genus])
            unmatched_data.append(specimen)
            continue

        if check_for_divergance(taxonomy_tree[order][family][genus], changes["Species"], species):
            unmatched_data.append(specimen)
            continue

    return unmatched_data, changes

def main():
    """Compares museum taxonomy data with the current accepted taxonomy"""
    parser = argparse.ArgumentParser(
                prog = 'compare_data.py',
                description = 'Compares museum taxonomy data with the current accepted taxonomy',
                epilog = 'Written as a collaboration between Jacob and Ezra')
    
    parser.add_argument("-tf", "--taxonomy_file", type=argparse.FileType('r', encoding="utf-8"), default="./out/taxonomy_tree.json")
    parser.add_argument("-rf", "--records_file", type=argparse.FileType('r', encoding="utf-8"), default="./mvz/mvz_data.csv")
    parser.add_argument("-or", "--out_diff_records", default="./out/diff_records.csv")
    parser.add_argument("-oc", "--out_diff_taxa", type=argparse.FileType('w', encoding="utf-8"), default="./out/diff_taxa.json")

    args = parser.parse_args()

    taxonomy_tree = json.load(args.taxonomy_file)
    museum_data_reader = csv.DictReader(args.records_file, delimiter=",")

    unmatched_data, changes = compare_data(taxonomy_tree, museum_data_reader)

    with open(args.out_diff_records, "w", encoding="utf-8", newline="") as out_records_file:
        data_writer = csv.DictWriter(out_records_file, fieldnames=unmatched_data[0].keys())

        data_writer.writeheader()
        for unmatched in unmatched_data:
            data_writer.writerow(unmatched)

    json.dump(changes, args.out_diff_taxa, indent=4)

if __name__ == "__main__":
    main()
