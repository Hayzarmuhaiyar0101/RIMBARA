
from modules.acquisition import search_sentinel2

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
    print("Tidak ada citra tersedia.")
    raise SystemExit

# Periksa aset produk pertama
item = items[0]

print("\n===== RIMBARA ASSET INSPECTION =====")
print("Product ID:", item.id)
print("Tanggal:", item.datetime)

print("\nDAFTAR BAND DAN ASET:")

for key, asset in item.assets.items():
    print(
        "Nama:", key,
        "| Tipe:", asset.media_type,
        "| URL tersedia:", bool(asset.href)
    )


required_bands = {
    "NIR": "B08_10m",
    "SWIR": "B12_20m",
    "CLOUD_MASK": "SCL_20m"
}

print("\n===== REQUIRED BAND VALIDATION =====")

for name, asset_key in required_bands.items():

    if asset_key in item.assets:
        asset = item.assets[asset_key]

        print(f"{name}: AVAILABLE")
        print(f"Asset: {asset_key}")
        print(f"Type: {asset.media_type}")
        print(f"URL: {asset.href[:100]}...")
    else:
        print(f"{name}: NOT AVAILABLE")

