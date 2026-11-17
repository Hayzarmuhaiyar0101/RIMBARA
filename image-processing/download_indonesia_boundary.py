
import json
import time
import requests
import geopandas as gpd

from pathlib import Path
from requests.exceptions import RequestException

# BIG ArcGIS REST API
API_URL = (
    "https://geoservices.big.go.id/rbi/rest/services/"
    "BATASWILAYAH/BATAS_KABKOTA_AR/MapServer/0/query"
)

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "data" / "boundaries"
OUTPUT_FILE = OUTPUT_DIR / "indonesia_kabkota.geojson"
CHECKPOINT_FILE = OUTPUT_DIR / "indonesia_kabkota_checkpoint.geojson"

# Download configuration
BATCH_SIZE = 25
MAX_RETRIES = 5
EXPECTED_COUNT = 541


def save_checkpoint(features, next_offset):
    """Menyimpan progres download agar dapat dilanjutkan."""

    geojson = {
        "type": "FeatureCollection",
        "rimbara_next_offset": next_offset,
        "features": list(features.values())
    }

    temp_file = CHECKPOINT_FILE.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(geojson, file, ensure_ascii=False)

    temp_file.replace(CHECKPOINT_FILE)


def download_boundaries():

    print("===== RIMBARA NATIONAL BOUNDARY DOWNLOAD =====")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    session = requests.Session()

    all_features = {}

    offset = 0

    # Memeriksa checkpoint sebelumnya
    if CHECKPOINT_FILE.exists():

        print("\nCheckpoint ditemukan.")
        print("Melanjutkan download sebelumnya...")

        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as file:
            checkpoint = json.load(file)

        for feature in checkpoint.get("features", []):
            object_id = feature.get("properties", {}).get("OBJECTID")

            if object_id is not None:
                all_features[object_id] = feature

        offset = checkpoint.get(
            "rimbara_next_offset",
            len(all_features)
        )

        print("Data tersimpan:", len(all_features))
        print("Melanjutkan dari record:", offset)

    while True:

        print(f"\nMengambil record mulai: {offset}")

        params = {
            "where": "1=1",
            "outFields": "*",
            "returnGeometry": "true",
            "outSR": 4326,
            "resultOffset": offset,
            "resultRecordCount": BATCH_SIZE,
            "orderByFields": "OBJECTID ASC",
            "f": "geojson"
        }

        response = None

        # Retry otomatis
        for attempt in range(1, MAX_RETRIES + 1):

            try:

                response = session.get(
                    API_URL,
                    params=params,
                    timeout=(20, 180)
                )

                response.raise_for_status()

                result = response.json()

                if "error" in result:
                    raise RuntimeError(result["error"])

                break

            except (RequestException, ValueError, RuntimeError) as error:

                print(
                    f"Percobaan {attempt}/{MAX_RETRIES} gagal: {error}"
                )

                if attempt == MAX_RETRIES:
                    raise RuntimeError(
                        "Download gagal setelah beberapa percobaan. "
                        "Checkpoint tetap disimpan."
                    ) from error

                wait_time = 5 * attempt

                print(f"Mencoba kembali dalam {wait_time} detik...")
                time.sleep(wait_time)

        features = result.get("features", [])

        if not features:
            break

        for feature in features:

            object_id = feature.get(
                "properties", {}
            ).get("OBJECTID")

            if object_id is None:
                raise ValueError(
                    "Fitur tidak memiliki OBJECTID."
                )

            all_features[object_id] = feature

        offset += len(features)

        # Simpan progres setiap batch
        save_checkpoint(all_features, offset)

        print("Data diterima:", len(features))
        print("Total tersimpan:", len(all_features))
        print("Progres:", f"{len(all_features)}/{EXPECTED_COUNT}")

        if len(features) < BATCH_SIZE:
            break

        time.sleep(1)

    if not all_features:
        raise RuntimeError("Tidak ada data geometri ditemukan.")

    # Susun GeoJSON final
    final_geojson = {
        "type": "FeatureCollection",
        "features": list(all_features.values())
    }

    temp_output = OUTPUT_FILE.with_suffix(".tmp")

    with open(temp_output, "w", encoding="utf-8") as file:
        json.dump(final_geojson, file, ensure_ascii=False)

    temp_output.replace(OUTPUT_FILE)

    print("\n===== DOWNLOAD COMPLETED =====")
    print("Total wilayah:", len(all_features))
    print("File:", OUTPUT_FILE)

    if len(all_features) == EXPECTED_COUNT:
        print("VALIDATION: 541 WILAYAH BERHASIL DIUNDUH")
    else:
        print(
            "PERHATIAN: Jumlah wilayah berbeda dari target 541."
        )

    # Hapus checkpoint setelah proses berhasil
    if CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()

    print("\nRIMBARA NATIONAL BOUNDARY READY!")


if __name__ == "__main__":
    download_boundaries()
