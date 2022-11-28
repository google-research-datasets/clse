"""Generates v1.1 Data.

From v1.0 data, we include additional columns containing parsed
attribute values for the superset of linguistic attributes across all
languages.
"""

import csv
from copy import copy
from typing import Dict, List

# Path to the corpus.
CORPUS_PATH = "data/clse_v1.0.csv"
NEW_CORPUS_PATH = "data/clse_v1.1.csv"

# List of linguistic signature prefixes.
VERBOSE_SIGNATURE_PREFIXES = [
    "NameTags.",
    "Variant.",
    "WordStemAnnotation.",
    "Common",
    "SurfaceForm.",
    "Determiner.",
    "Proper",
]


def get_concise_attribute(attribute_name: str) -> str:
    """Returns a concise name of the linguistic attribute."""
    concise_attribute_name = attribute_name
    for prefix in VERBOSE_SIGNATURE_PREFIXES:
        concise_attribute_name = concise_attribute_name.removeprefix(prefix)
    return concise_attribute_name


def get_linguistic_attribute_dict(linguistic_signature: str) -> Dict[str, str]:
    """Returns a dictionary of linguistic attribute -> value."""
    # Split the signature into constituent parts, where each element is an 'attribute:value' string.
    attribute_values = linguistic_signature.split(",")

    # Parse attributes into a map.
    attribute_map = {}
    for attribute_value in attribute_values:
        if not attribute_value:
            continue

        attribute_name, value = attribute_value.split(":", 1)
        attribute_map[get_concise_attribute(attribute_name)] = value

    return attribute_map


def get_all_attributes() -> List[str]:
    """Returns a sorted list of the superset of all linguistic attributes over all languages."""
    all_attributes = set()
    with open(CORPUS_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            attribute_map = get_linguistic_attribute_dict(row["linguistic_signature"])
            all_attributes.update(attribute_map.keys())
    return sorted(all_attributes)


def main():
    # Pre-existing 1.0 column names.
    fieldnames = ["language", "mid", "name", "linguistic_signature", "semantic_type"]

    # Add the superset of all linguistic attributes as additional columns.
    fieldnames.extend(get_all_attributes())

    with open(NEW_CORPUS_PATH, "w") as new_f:
        writer = csv.DictWriter(new_f, fieldnames=fieldnames)
        writer.writeheader()
        with open(CORPUS_PATH) as f:
            reader = csv.DictReader(f)
            new_row = {}
            for row in reader:
                new_row = copy(row)
                attribute_map = get_linguistic_attribute_dict(
                    row["linguistic_signature"]
                )
                new_row.update(attribute_map)
                writer.writerow(new_row)

    print(f"Finished writing data to {NEW_CORPUS_PATH}!")


if __name__ == "__main__":
    main()
