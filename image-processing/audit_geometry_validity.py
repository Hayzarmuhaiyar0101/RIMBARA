
import json
from pathlib import Path
from collections import Counter

from shapely.geometry import shape
from shapely.validation import explain_validity


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "boundaries"
    / "geometry_checkpoint.json"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "boundaries"
    / "geometry_validity_audit.csv"
)


def main():

    print("===== RIMBARA GEOMETRY VALIDITY AUDIT =====")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    total = 0
    valid_count = 0
    invalid_count = 0
    empty_count = 0

    geometry_types = Counter()
    invalid_records = []

    for oid, record in records.items():

        total += 1

        try:
            geometry_data = record["geometry"]

            geom = shape({
                "type": "Polygon",
                "coordinates": geometry_data["rings"]
            })

            geometry_types[geom.geom_type] += 1

            if geom.is_empty:
                empty_count += 1
                status = "EMPTY"
                reason = "Empty geometry"

            elif geom.is_valid:
                valid_count += 1
                status = "VALID"
                reason = ""

            else:
                invalid_count += 1
                status = "INVALID"
                reason = explain_validity(geom)

            if status != "VALID":
                attrs = record.get("attributes", {})

                invalid_records.append({
                    "OBJECTID": oid,
                    "NAME": attrs.get("namobj", ""),
                    "STATUS": status,
                    "REASON": reason
                })

        except Exception as e:

            invalid_count += 1

            invalid_records.append({
                "OBJECTID": oid,
                "NAME": "",
                "STATUS": "ERROR",
                "REASON": str(e)
            })

    print("\n===== AUDIT SUMMARY =====")
    print("Total records :", total)
    print("Valid         :", valid_count)
    print("Invalid       :", invalid_count)
    print("Empty         :", empty_count)

    print("\n===== GEOMETRY TYPES =====")

    for name, count in geometry_types.items():
        print(f"{name}: {count}")

    print("\n===== INVALID RECORDS =====")

    for item in invalid_records:
        print(item)

    import pandas as pd

    pd.DataFrame(invalid_records).to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nAudit report:", OUTPUT_FILE)

    print("\n===== AUDIT COMPLETED =====")


if __name__ == "__main__":
    main()
