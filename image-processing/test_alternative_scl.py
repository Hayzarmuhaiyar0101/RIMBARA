
import rasterio
import numpy as np
from pathlib import Path

from modules.acquisition import search_sentinel2
from modules.download import create_s3_client, download_asset

BBOX = [
    113.70, -2.35,
    114.10, -1.80
]

OLD_PRODUCT = (
    "S2C_MSIL2A_20260320T022531_"
    "N0512_R046_T49MHU_20260320T061512"
)


def main():

    print("===== ALTERNATIVE SCL TEST =====")

    items = search_sentinel2(
        bbox=BBOX,
        start_date="2026-03-01",
        end_date="2026-04-30",
        max_cloud=30,
        max_items=10
    )

    candidates = [
        item for item in items
        if item.id != OLD_PRODUCT
    ][:5]

    if not candidates:
        print("Tidak ada produk alternatif.")
        return

    s3_client = create_s3_client()

    output_dir = Path("data/raw/alternative_scl")
    output_dir.mkdir(parents=True, exist_ok=True)

    for item in candidates:

        print("\n--------------------------------")
        print("PRODUCT:", item.id)
        print("DATE:", item.datetime)

        if "SCL_20m" not in item.assets:
            print("SCL_20m tidak tersedia.")
            continue

        output_path = output_dir / f"{item.id}_SCL_20m.jp2"

        if not output_path.exists():
            download_asset(
                s3_client,
                item.assets["SCL_20m"],
                output_path
            )

        with rasterio.open(output_path) as src:

            data = src.read(1)

            values, counts = np.unique(
                data,
                return_counts=True
            )

            print("Resolution:", src.res)
            print("File size (MB):", round(
                output_path.stat().st_size / (1024 * 1024),
                4
            ))

            print("CLASS DISTRIBUTION:")

            for value, count in zip(values, counts):

                percentage = count / data.size * 100

                print(
                    f"Class {value}: "
                    f"{count:,} pixels "
                    f"({percentage:.2f}%)"
                )

            valid_classes = set(values) - {0, 1}

            if valid_classes:
                print("RESULT: OTHER CLASSES FOUND")
            else:
                print("RESULT: ONLY CLASS 0 AND 1")

    print("\n===== ALTERNATIVE TEST COMPLETED =====")


if __name__ == "__main__":
    main()
