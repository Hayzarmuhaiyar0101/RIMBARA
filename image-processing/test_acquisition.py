
from modules.acquisition import search_sentinel2

# Wilayah pengujian Palangka Raya
bbox = [
    113.70, -2.35,
    114.10, -1.80
]

items = search_sentinel2(
    bbox=bbox,
    start_date="2024-01-01",
    end_date="2026-11-11",
    max_cloud=30,
    max_items=100
)

if items:
    print("\nRIMBARA: DATA SENTINEL-2 DITEMUKAN!")
else:
    print("\nTidak ada citra yang ditemukan.")
