
from modules.acquisition import search_sentinel2

PRODUCT_ID = (
    "S2C_MSIL2A_20260320T022531_"
    "N0512_R046_T49MHU_20260320T061512"
)

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

item = next(
    (x for x in items if x.id == PRODUCT_ID),
    None
)

if item is None:
    raise SystemExit("Produk tidak ditemukan.")

print("\n===== RIMBARA SCL ASSET AUDIT =====")
print("Product ID:", item.id)
print("Product datetime:", item.datetime)

for key in ["SCL_20m", "SCL_60m", "B08_10m", "B12_20m"]:

    print(f"\n===== {key} =====")

    if key not in item.assets:
        print("Asset tidak tersedia.")
        continue

    asset = item.assets[key]

    print("Media type:", asset.media_type)
    print("Title:", asset.title)
    print("Roles:", asset.roles)
    print("Href:", asset.href)

    print("Extra fields:", asset.extra_fields)

print("\n===== AUDIT COMPLETED =====")
