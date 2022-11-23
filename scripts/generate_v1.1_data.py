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
    "InflectedNounForm.",
    "NominalInflectedForm.",
    "NameTags.",
    "Variant.",
    "WordStemAnnotation.",
    "Common",
    "SurfaceForm.",
    "Determiner.",
    "Proper",
    "InflectedForm.",
]


def get_linguistic_attribute_dict(linguistic_signature: str) -> Dict[str, str]:
    """Returns a dictionary of linguistic attribute -> value."""
    # Strip verbose prefixes from the linguistic signature.
    reduced_linguistic_signature = linguistic_signature
    for verbose_signature_prefix in VERBOSE_SIGNATURE_PREFIXES:
        reduced_linguistic_signature = reduced_linguistic_signature.replace(
            verbose_signature_prefix, ""
        )

    # Split the signature into constituent parts.
    attributes = reduced_linguistic_signature.split(",")

    # Parse attributes into a map.
    attribute_map = {}
    for attribute in attributes:
        if not attribute:
            continue
        components = attribute.split(":")
        attribute_map[components[0]] = components[1]

    return attribute_map


def get_all_attributes() -> List[str]:
    """Returns a sorted list of the superset of all linguistic attributes."""
    all_attributes = set()
    with open(CORPUS_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            attribute_map = get_linguistic_attribute_dict(row["linguistic_signature"])
            all_attributes.update(list(attribute_map.keys()))
    return sorted(list(all_attributes))


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
