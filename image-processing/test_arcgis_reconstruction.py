
import json
from pathlib import Path

from shapely.geometry import Polygon, MultiPolygon
from shapely.validation import explain_validity


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    BASE_DIR / "data" / "boundaries"
    / "geometry_checkpoint.json"
)


def signed_area(ring):
    area = 0.0

    for i in range(len(ring) - 1):
        x1, y1 = ring[i][:2]
        x2, y2 = ring[i + 1][:2]
        area += x1 * y2 - x2 * y1

    return area / 2


def reconstruct(rings):

    exteriors = []
    interiors = []

    for index, ring in enumerate(rings):

        area = signed_area(ring)
        polygon = Polygon(ring)

        item = {
            "index": index,
            "ring": ring,
            "polygon": polygon,
            "area": abs(area)
        }

        if area < 0:
            exteriors.append(item)
        elif area > 0:
            interiors.append(item)

    polygons = []

    for exterior in exteriors:

        holes = []

        for interior in interiors:

            if exterior["polygon"].covers(
                interior["polygon"]
            ):
                holes.append(interior["ring"])

        polygons.append(
            Polygon(
                exterior["ring"],
                holes
            )
        )

    if len(polygons) == 1:
        result = polygons[0]
    else:
        result = MultiPolygon(polygons)

    return result, len(exteriors), len(interiors)


def main():

    with open(INPUT_FILE, encoding="utf-8") as f:
        records = json.load(f)

    print("===== ARCGIS RECONSTRUCTION TEST =====")

    for oid in ["2", "3", "8", "257", "532"]:

        record = records[oid]
        rings = record["geometry"]["rings"]

        geom, exterior_count, interior_count = (
            reconstruct(rings)
        )

        print("\n-------------------------------")
        print("OBJECTID:", oid)
        print("NAME:", record["attributes"].get("namobj"))
        print("Exterior:", exterior_count)
        print("Interior:", interior_count)
        print("Geometry:", geom.geom_type)
        print("Valid:", geom.is_valid)
        print("Empty:", geom.is_empty)
        print("Area:", geom.area)

        if not geom.is_valid:
            print("Reason:", explain_validity(geom))

        if geom.geom_type == "MultiPolygon":
            print("Polygon count:", len(geom.geoms))

    print("\n===== TEST COMPLETED =====")


if __name__ == "__main__":
    main()
