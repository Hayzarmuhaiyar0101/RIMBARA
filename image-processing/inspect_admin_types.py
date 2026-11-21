
import requests
import pandas as pd

from pathlib import Path

API_URL = (
    "https://geoservices.big.go.id/rbi/rest/services/"
    "BATASWILAYAH/BATAS_WILAYAH/MapServer/13/query"
)

BASE_DIR = Path(__file__).resolve().parent

CSV_FILE = (
    BASE_DIR / "data" / "boundaries"
    / "national_boundary_audit.csv"
)


def inspect_types():

    print("===== RIMBARA ADMIN TYPE INVESTIGATION =====")

    df = pd.read_csv(CSV_FILE)

    for admin_type in sorted(df["TIPADM"].dropna().unique()):

        print(f"\n===== TIPADM {admin_type} =====")

        subset = df[df["TIPADM"] == admin_type]

        print("Jumlah fitur:", len(subset))

        print(
            subset[
                ["OBJECTID", "NAMOBJ", "KDPKAB",
                 "WADMKK", "WADMPR"]
            ].head(10).to_string(index=False)
        )

    print("\n===== BIG LAYER METADATA =====")

    response = requests.get(
        API_URL.replace("/query", ""),
        params={"f": "json"},
        timeout=(20, 120)
    )

    response.raise_for_status()

    metadata = response.json()

    print("Layer:", metadata.get("name"))
    print("Description:", metadata.get("description"))

    for field in metadata.get("fields", []):

        if field.get("name", "").upper() == "TIPADM":

            print("\nTIPADM FIELD:")
            print(field)

    print("\n===== INVESTIGATION COMPLETED =====")


if __name__ == "__main__":
    inspect_types()
