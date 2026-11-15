
import rasterio
import numpy as np
from pathlib import Path

from modules.acquisition import search_sentinel2
from modules.download import create_s3_client, download_asset


PRODUCT_ID = (
    "S2C_MSIL2A_20260320T022531_"
    "N0512_R046_T49MHU_20260320T061512"
)

BBOX = [
    113.70, -2.35,
    114.10, -1.80
]


def inspect_scl(label, path):

    print(f"\n===== {label} =====")

    with rasterio.open(path, OVERVIEW_LEVEL="NONE") as src:

        data = src.read(1)

        values, counts = np.unique(
            data,
            return_counts=True
        )

        print("Shape:", data.shape)
        print("Resolution:", src.res)
        print("File size:", round(
            Path(path).stat().st_size / (1024 * 1024), 4
        ), "MB")

        print("\nDistribusi kelas:")

        for value, count in zip(values, counts):
            print(
                f"Class {value}: "
                f"{count:,} pixels "
                f"({count / data.size * 100:.2f}%)"
            )


def main():

    print("===== RIMBARA SCL COMPARISON =====")

    items = search_sentinel2(
        bbox=BBOX,
        start_date="2026-03-01",
        end_date="2026-04-30",
        max_cloud=30,
        max_items=10
    )

    item = next(
        (x for x in items if x.id == PRODUCT_ID),
        None
    )

    if item is None:
        print("Produk tidak ditemukan.")
        return

    print("Product:", item.id)

    if "SCL_60m" not in item.assets:
        print("SCL_60m tidak tersedia.")
        return

    output_dir = Path("data/raw/diagnostic")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "SCL_60m.jp2"

    if not output_path.exists():

        s3_client = create_s3_client()

        download_asset(
            s3_client,
            item.assets["SCL_60m"],
            output_path
        )

    original_path = (
        Path("data/raw/post_fire")
        / PRODUCT_ID
        / "SCL_20m.jp2"
    )

    inspect_scl("SCL 20M", original_path)
    inspect_scl("SCL 60M", output_path)

    print("\n===== COMPARISON COMPLETED =====")


if __name__ == "__main__":
    main()
