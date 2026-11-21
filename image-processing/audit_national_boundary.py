
import requests
import pandas as pd

from pathlib import Path

API_URL = (
    "https://geoservices.big.go.id/rbi/rest/services/"
    "BATASWILAYAH/BATAS_WILAYAH/MapServer/13/query"
)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "data" / "boundaries"

BATCH_SIZE = 100


def audit_boundary():

    print("===== RIMBARA NATIONAL BOUNDARY AUDIT =====")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    session = requests.Session()

    all_records = []
    offset = 0

    # Mengambil seluruh atribut
    while True:

        print(f"\nMemeriksa record: {offset}")

        params = {
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "false",
            "resultOffset": offset,
            "resultRecordCount": BATCH_SIZE,
            "orderByFields": "OBJECTID ASC",
            "f": "json"
        }

        response = session.get(
            API_URL,
            params=params,
            timeout=(20, 120)
        )

        response.raise_for_status()

        result = response.json()

        if "error" in result:
            raise RuntimeError(result["error"])

        features = result.get("features", [])

        if not features:
            break

        for feature in features:
            all_records.append(feature["attributes"])

        print("Data diterima:", len(features))
        print("Total:", len(all_records))

        offset += len(features)

        if len(features) < BATCH_SIZE:
            break

    # Membuat DataFrame
    df = pd.DataFrame(all_records)

    if df.empty:
        raise RuntimeError("Data audit kosong.")

    # Normalisasi nama kolom
    df.columns = [str(col).upper() for col in df.columns]

    print("\nKolom ditemukan:")
    print(df.columns.tolist())

    required_columns = [
        "OBJECTID",
        "NAMOBJ",
        "KDPKAB",
        "KDPPUM",
        "WADMKK",
        "WADMPR",
        "TIPADM",
        "METADATA"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise RuntimeError(f"Field tidak ditemukan: {missing}")

    # Normalisasi nilai teks
    for column in ["NAMOBJ", "KDPKAB", "WADMKK", "WADMPR"]:
        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    # Audit kelengkapan
    print("\n===== COMPLETENESS AUDIT =====")

    print("Total fitur:", len(df))
    print("Nama kosong:", (df["NAMOBJ"] == "").sum())
    print("Kode KDPKAB kosong:", (df["KDPKAB"] == "").sum())
    print("Nama WADMKK kosong:", (df["WADMKK"] == "").sum())
    print("Provinsi kosong:", (df["WADMPR"] == "").sum())

    # Audit kode wilayah
    print("\n===== CODE AUDIT =====")

    valid_codes = df.loc[
        df["KDPKAB"] != "", "KDPKAB"
    ]

    print("Kode unik:", valid_codes.nunique())

    duplicates = df[
        (df["KDPKAB"] != "") &
        df["KDPKAB"].duplicated(keep=False)
    ]

    print("Baris dengan kode duplikat:", len(duplicates))

    if not duplicates.empty:
        print(
            duplicates[
                ["NAMOBJ", "KDPKAB", "WADMPR"]
            ].to_string(index=False)
        )

    # Audit tipe administrasi
    print("\n===== ADMINISTRATIVE TYPE =====")

    print(df["TIPADM"].value_counts(dropna=False))

    # Audit provinsi
    print("\n===== PROVINCE COVERAGE =====")

    provinces = sorted(
        value for value in df["WADMPR"].unique()
        if value
    )

    print("Jumlah nama provinsi:", len(provinces))

    for province in provinces:
        count = (df["WADMPR"] == province).sum()
        print(f"{province}: {count}")

    # Simpan hasil audit
    output_file = OUTPUT_DIR / "national_boundary_audit.csv"

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n===== AUDIT COMPLETED =====")
    print("File:", output_file)


if __name__ == "__main__":
    audit_boundary()
