
import ijson
import pandas as pd

from pathlib import Path
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely.validation import make_valid


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "boundaries"

GEOMETRY_FILE = (
    DATA_DIR / "geometry_checkpoint.json"
)

REGENCY_FILE = (
    DATA_DIR / "national_regencies.csv"
)

CITY_FILE = (
    DATA_DIR / "national_cities.csv"
)



def ring_area(ring):
    """Menghitung signed area menggunakan float."""

    area = 0.0

    for i in range(len(ring) - 1):

        x1, y1 = map(float, ring[i])
        x2, y2 = map(float, ring[i + 1])

        area += (x1 * y2) - (x2 * y1)

    return area / 2.0



def esri_geometry_to_shapely(geometry):
    """
    Mengubah ESRI polygon rings menjadi Shapely geometry.

    ESRI:
    - Outer ring: clockwise
    - Inner ring: counterclockwise
    """

    rings = geometry.get("rings", [])

    shells = []
    holes = []

    for ring in rings:

        if len(ring) < 4:
            continue

        area = ring_area(ring)

        if area < 0:
            shells.append(ring)

        elif area > 0:
            holes.append(ring)

    polygons = []

    for shell in shells:

        shell_polygon = Polygon(shell)

        if shell_polygon.is_empty:
            continue

        assigned_holes = []

        for hole in holes:

            hole_polygon = Polygon(hole)

            if shell_polygon.covers(
                hole_polygon.representative_point()
            ):
                assigned_holes.append(hole)

        polygon = Polygon(
            shell,
            assigned_holes
        )

        if not polygon.is_valid:
            polygon = make_valid(polygon)

        if not polygon.is_empty:
            polygons.append(polygon)

    if not polygons:
        raise ValueError(
            "Tidak ditemukan polygon valid dalam geometri."
        )

    result = unary_union(polygons)

    if not result.is_valid:
        result = make_valid(result)

    return result


def load_admin_database():

    regencies = pd.read_csv(
        REGENCY_FILE,
        dtype=str
    )

    cities = pd.read_csv(
        CITY_FILE,
        dtype=str
    )

    return pd.concat(
        [regencies, cities],
        ignore_index=True
    )


def get_expected_codes(province=None):

    data = load_admin_database()

    data["KDPKAB"] = (
        data["KDPKAB"].fillna("").str.strip()
    )

    if province:
        data = data[
            data["WADMPR"].str.casefold()
            == province.strip().casefold()
        ]

    return set(
        data.loc[
            data["KDPKAB"] != "",
            "KDPKAB"
        ].unique()
    )


def get_aoi_geometry(
    province=None,
    admin_code=None,
    allow_incomplete=False
):
    """
    Mengambil dan menggabungkan polygon AOI.

    province:
        Nama provinsi.

    admin_code:
        Kode kabupaten/kota.

    allow_incomplete:
        Mengizinkan hasil parsial jika geometri belum lengkap.
    """

    if not GEOMETRY_FILE.exists():
        raise FileNotFoundError(
            "Geometry checkpoint tidak ditemukan."
        )

    if province is None and admin_code is None:
        raise ValueError(
            "Tentukan province atau admin_code."
        )

    if admin_code:
        admin_code = str(admin_code).strip()

    expected_codes = get_expected_codes(province)

    if admin_code:
        if admin_code not in expected_codes:
            raise ValueError(
                f"Kode administrasi tidak ditemukan: {admin_code}"
            )

        expected_codes = {admin_code}

    geometries = []
    found_codes = set()

    print("===== RIMBARA AOI PROCESSOR =====")

    with open(
        GEOMETRY_FILE,
        "rb"
    ) as file:

        for objectid, record in ijson.kvitems(
            file, ""
        ):

            attributes = record.get(
                "attributes", {}
            )

            code = str(
                attributes.get("kdpkab", "")
            ).strip()

            province_name = str(
                attributes.get("wadmpr", "")
            ).strip()

            admin_type = attributes.get(
                "tipadm"
            )

            if admin_type not in (4, 5):
                continue

            if code not in expected_codes:
                continue

            if province and (
                province_name.casefold()
                != province.strip().casefold()
            ):
                continue

            geometry = record.get("geometry")

            if not geometry:
                continue

            try:

                polygon = esri_geometry_to_shapely(
                    geometry
                )

                geometries.append(polygon)
                found_codes.add(code)

            except Exception as error:

                print(
                    f"Geometri gagal {objectid}: {error}"
                )

    missing_codes = expected_codes - found_codes

    print("Kode ditemukan:", len(found_codes))
    print("Kode belum tersedia:", len(missing_codes))

    if missing_codes and not allow_incomplete:

        raise RuntimeError(
            "AOI belum lengkap. "
            f"Kode yang belum memiliki geometri: "
            f"{sorted(missing_codes)}"
        )

    if not geometries:
        raise RuntimeError(
            "Tidak ada geometri yang berhasil diproses."
        )

    result = unary_union(geometries)

    if not result.is_valid:
        result = make_valid(result)

    print("AOI berhasil dibentuk.")
    print("Geometry type:", result.geom_type)
    print("Bounds:", result.bounds)

    return result


def get_aoi_bbox(geometry):

    west, south, east, north = geometry.bounds

    return (
        west,
        south,
        east,
        north
    )


def get_national_aoi(allow_incomplete=False):

    return get_aoi_geometry(
        allow_incomplete=allow_incomplete
    )


def get_province_aoi(
    province,
    allow_incomplete=False
):

    return get_aoi_geometry(
        province=province,
        allow_incomplete=allow_incomplete
    )


def get_region_aoi(
    admin_code,
    allow_incomplete=False
):

    return get_aoi_geometry(
        admin_code=admin_code,
        allow_incomplete=allow_incomplete
    )
