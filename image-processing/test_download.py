
from pathlib import Path

from modules.acquisition import search_sentinel2
from modules.download import download_required_bands


def main():

    bbox = [
        113.70, -2.35,
        114.10, -1.80
    ]

    items = search_sentinel2(
        bbox=bbox,
        start_date="2026-03-01",
        end_date="2026-04-30",
        max_cloud=30,
        max_items=10
    )

    if not items:
        print("Tidak ada citra ditemukan.")
        return

    item = items[0]

    print("\n===== RIMBARA DOWNLOAD TEST =====")
    print("Product:", item.id)
    print("Tanggal:", item.datetime)

    output_dir = (
        Path("data")
        / "raw"
        / "post_fire"
        / item.id
    )

    downloaded = download_required_bands(
        item,
        output_dir
    )

    print("\n===== DOWNLOAD COMPLETED =====")

    for band, path in downloaded.items():
        print(band, ":", path)


if __name__ == "__main__":
    main()
