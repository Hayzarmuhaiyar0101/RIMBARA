
import json
import time
import requests
import geopandas as gpd

from pathlib import Path
from shapely.geometry import shape
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ==========================================
# RIMBARA NATIONAL GEOMETRY DOWNLOADER
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data" / "boundaries"

OUTPUT_FILE = DATA_DIR / "indonesia_national_esrijson.json"
CHECKPOINT_FILE = DATA_DIR / "geometry_checkpoint.json"
FAILED_FILE = DATA_DIR / "failed_objectids.json"

API_URL = (
    "https://geoservices.big.go.id/rbi/rest/services/"
    "BATASWILAYAH/BATAS_WILAYAH/MapServer/13/query"
)

TOTAL_FEATURES = 539

REQUEST_DELAY = 3
MAX_RETRIES = 5


# ==========================================
# SESSION CONFIGURATION
# ==========================================

def create_session():

    session = requests.Session()

    retry = Retry(
        total=MAX_RETRIES,
        connect=MAX_RETRIES,
        read=MAX_RETRIES,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry)

    session.mount("https://", adapter)

    session.headers.update({
        "User-Agent": "RIMBARA-National-Monitor/1.0"
    })

    return session


# ==========================================
# CHECKPOINT
# ==========================================

def load_checkpoint():

    if not CHECKPOINT_FILE.exists():
        return {}

    with open(CHECKPOINT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_checkpoint(records):

    temporary_file = CHECKPOINT_FILE.with_suffix(".tmp")

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False)

    temporary_file.replace(CHECKPOINT_FILE)


# ==========================================
# DOWNLOAD SINGLE GEOMETRY
# ==========================================

def download_geometry(session, object_id):

    params = {
        "where": f"objectid = {object_id}",
        "outFields": "*",
        "returnGeometry": "true",
        "outSR": 4326,
        "f": "json"
    }

    response = session.get(
        API_URL,
        params=params,
        timeout=(30, 180)
    )

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise RuntimeError(data["error"])

    features = data.get("features", [])

    if len(features) != 1:
        raise RuntimeError(
            f"OBJECTID {object_id}: fitur tidak ditemukan."
        )

    feature = features[0]

    geometry = feature.get("geometry")

    if not geometry or not geometry.get("rings"):
        raise RuntimeError(
            f"OBJECTID {object_id}: geometri kosong."
        )

    return feature


# ==========================================
# VALIDATE GEOMETRY
# ==========================================


def validate_feature(feature):

    geometry = feature.get("geometry")

    if not geometry:
        return False

    rings = geometry.get("rings")

    if not rings:
        return False

    if not isinstance(rings, list):
        return False

    # Pastikan setiap ring memiliki minimal
    # empat koordinat untuk membentuk polygon.
    for ring in rings:

        if not isinstance(ring, list):
            return False

        if len(ring) < 4:
            return False

        if ring[0] != ring[-1]:
            return False

    return True



# ==========================================
# SAVE GEOJSON
# ==========================================

def save_geojson(records):

    features = list(records.values())

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    temporary_file = OUTPUT_FILE.with_suffix(".tmp")

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(geojson, file, ensure_ascii=False)

    temporary_file.replace(OUTPUT_FILE)


# ==========================================
# MAIN PROCESS
# ==========================================

def main():

    print("=" * 55)
    print("RIMBARA NATIONAL GEOMETRY DOWNLOADER")
    print("=" * 55)

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    session = create_session()

    records = load_checkpoint()

    completed = set(records.keys())

    failed = []

    print("Target fitur:", TOTAL_FEATURES)
    print("Sudah tersimpan:", len(records))

    for object_id in range(1, TOTAL_FEATURES + 1):

        key = str(object_id)

        if key in completed:
            continue

        print(f"\nMengunduh OBJECTID {object_id}...")

        try:

            feature = download_geometry(
                session,
                object_id
            )

            if not validate_feature(feature):
                raise RuntimeError("Geometri tidak valid.")

            records[key] = feature

            save_checkpoint(records)

            print(
                "BERHASIL:",
                feature["attributes"].get("namobj")
            )

            print(
                f"Progres: {len(records)}/{TOTAL_FEATURES}"
            )

            # Simpan GeoJSON sementara secara berkala
            if len(records) % 10 == 0:
                save_geojson(records)
                print("Checkpoint GeoJSON diperbarui.")

        except Exception as error:

            print("GAGAL:", error)

            failed.append({
                "objectid": object_id,
                "error": str(error)
            })

        time.sleep(REQUEST_DELAY)

    # ======================================
    # FINAL SAVE
    # ======================================

    save_checkpoint(records)
    save_geojson(records)

    with open(FAILED_FILE, "w", encoding="utf-8") as file:
        json.dump(failed, file, indent=4, ensure_ascii=False)

    print("\n" + "=" * 55)
    print("RIMBARA DOWNLOAD SUMMARY")
    print("=" * 55)

    print("Target:", TOTAL_FEATURES)
    print("Berhasil:", len(records))
    print("Gagal:", len(failed))

    print("GeoJSON:", OUTPUT_FILE)
    print("Checkpoint:", CHECKPOINT_FILE)
    print("Failed IDs:", FAILED_FILE)

    print("\nDOWNLOAD PROCESS COMPLETED")


if __name__ == "__main__":
    main()
