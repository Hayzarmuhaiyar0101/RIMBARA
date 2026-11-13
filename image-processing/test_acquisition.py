
from modules.acquisition import search_sentinel2


def main():

    bbox = [
        113.70, -2.35,
        114.10, -1.80
    ]

    items = search_sentinel2(
        bbox=bbox,
        start_date="2025-01-01",
        end_date="2026-11-11",
        max_cloud=30,
        max_items=50
    )

    if items:
        print("\nRIMBARA: SENTINEL-2 DATA FOUND!")
    else:
        print("\nTidak ada citra yang memenuhi kriteria.")


if __name__ == "__main__":
    main()
