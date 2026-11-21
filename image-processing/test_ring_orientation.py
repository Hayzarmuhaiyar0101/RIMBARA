
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "boundaries"
    / "geometry_checkpoint.json"
)


def calculate_signed_area(ring):
    area = 0.0

    for i in range(len(ring) - 1):
        x1, y1 = ring[i][:2]
        x2, y2 = ring[i + 1][:2]

        area += (x1 * y2) - (x2 * y1)

    return area / 2


def main():

    print("===== RIMBARA RING ORIENTATION AUDIT =====")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    sample_ids = ["2", "3", "8", "257", "532"]

    for oid in sample_ids:

        record = records.get(oid)

        if not record:
            print(f"\nOBJECTID {oid}: NOT FOUND")
            continue

        attrs = record["attributes"]
        rings = record["geometry"]["rings"]

        print("\n--------------------------------")
        print("OBJECTID :", oid)
        print("NAME     :", attrs.get("namobj"))
        print("TOTAL RINGS:", len(rings))

        for index, ring in enumerate(rings):

            area = calculate_signed_area(ring)

            orientation = (
                "CLOCKWISE" if area < 0
                else "COUNTERCLOCKWISE"
                if area > 0
                else "ZERO"
            )

            print(
                f"Ring {index + 1}: "
                f"Points={len(ring)}, "
                f"Area={area:.10f}, "
                f"Orientation={orientation}"
            )

    print("\n===== AUDIT COMPLETED =====")


if __name__ == "__main__":
    main()
