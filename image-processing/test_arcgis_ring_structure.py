
import json
from pathlib import Path
from collections import Counter

from shapely.geometry import LinearRing, Polygon
from shapely.prepared import prep


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


def main():

    with open(INPUT_FILE, encoding="utf-8") as f:
        records = json.load(f)

    print("===== ARCGIS RING STRUCTURE AUDIT =====")

    samples = ["2", "3", "8", "257", "532"]

    for oid in samples:

        record = records.get(oid)

        if not record:
            continue

        rings = record["geometry"]["rings"]
        attrs = record["attributes"]

        ring_data = []

        for index, coords in enumerate(rings):

            try:
                polygon = Polygon(coords)

                ring_data.append({
                    "index": index,
                    "coords": coords,
                    "polygon": polygon,
                    "area": abs(signed_area(coords)),
                    "orientation": (
                        "CW" if signed_area(coords) < 0
                        else "CCW"
                    )
                })

            except Exception as e:
                print("Ring error:", oid, index, e)

        ring_data.sort(
            key=lambda item: item["area"],
            reverse=True
        )

        parents = {}

        for i, child in enumerate(ring_data):

            child_polygon = child["polygon"]
            child_point = child_polygon.representative_point()

            candidates = []

            for j, parent in enumerate(ring_data):

                if i == j:
                    continue

                if parent["area"] <= child["area"]:
                    continue

                if parent["polygon"].covers(child_point):
                    candidates.append(parent)

            if candidates:
                nearest = min(
                    candidates,
                    key=lambda item: item["area"]
                )

                parents[child["index"]] = nearest["index"]
            else:
                parents[child["index"]] = None

        roots = sum(
            1 for parent in parents.values()
            if parent is None
        )

        children = len(parents) - roots

        print("\n--------------------------------")
        print("OBJECTID:", oid)
        print("NAME:", attrs.get("namobj"))
        print("TOTAL RINGS:", len(rings))
        print("POTENTIAL EXTERIORS:", roots)
        print("POTENTIAL INTERIORS:", children)

        print("RING RELATIONSHIPS:")

        for index, parent in parents.items():
            print(
                f"Ring {index + 1} -> "
                f"Parent: "
                f"{parent + 1 if parent is not None else 'NONE'}"
            )

    print("\n===== AUDIT COMPLETED =====")


if __name__ == "__main__":
    main()
