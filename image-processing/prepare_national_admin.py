
import pandas as pd

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    BASE_DIR / "data" / "boundaries"
    / "national_boundary_audit.csv"
)

OUTPUT_DIR = BASE_DIR / "data" / "boundaries"


def prepare_database():

    print("===== RIMBARA NATIONAL ADMIN DATABASE =====")

    df = pd.read_csv(INPUT_FILE)

    # Normalisasi nama kolom
    df.columns = [col.upper() for col in df.columns]

    # Pisahkan berdasarkan tipe administrasi
    provinces = df[df["TIPADM"] == 6].copy()

    regencies = df[df["TIPADM"] == 4].copy()

    cities = df[df["TIPADM"] == 5].copy()

    # Validasi struktur
    assert len(provinces) == 19
    assert len(regencies) == 422
    assert len(cities) == 98

    # Pastikan kode kabupaten/kota tersedia
    assert regencies["KDPKAB"].notna().all()
    assert cities["KDPKAB"].notna().all()

    # Simpan database
    provinces.to_csv(
        OUTPUT_DIR / "national_provinces.csv",
        index=False,
        encoding="utf-8-sig"
    )

    regencies.to_csv(
        OUTPUT_DIR / "national_regencies.csv",
        index=False,
        encoding="utf-8-sig"
    )

    cities.to_csv(
        OUTPUT_DIR / "national_cities.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n===== DATABASE SUMMARY =====")

    print("Provinsi:", len(provinces))
    print("Kabupaten:", len(regencies))
    print("Kota:", len(cities))

    print("\n===== DATABASE COMPLETED =====")


if __name__ == "__main__":
    prepare_database()
