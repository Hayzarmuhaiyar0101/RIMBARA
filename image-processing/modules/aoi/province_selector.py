from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "boundaries"

FILES = [
    DATA_DIR / "national_regencies.csv",
    DATA_DIR / "national_cities.csv",
]


def load_admin_data():
    frames = []

    for file in FILES:
        if not file.exists():
            raise FileNotFoundError(f"Database tidak ditemukan: {file}")

        df = pd.read_csv(file, dtype=str)
        frames.append(df)

    data = pd.concat(frames, ignore_index=True)

    for column in ["NAMOBJ", "WADMPR", "KDPKAB"]:
        data[column] = data[column].fillna("").str.strip()

    return data


def get_provinces():
    data = load_admin_data()

    provinces = sorted(
        province
        for province in data["WADMPR"].unique()
        if province
    )

    return provinces


if __name__ == "__main__":
    provinces = get_provinces()

    print("===== RIMBARA PROVINCE SELECTOR =====")
    print("Total provinsi:", len(provinces))

    for number, province in enumerate(provinces, 1):
        print(f"{number:02d}. {province}")
