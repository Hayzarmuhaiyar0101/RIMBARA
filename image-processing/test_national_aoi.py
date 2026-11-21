
from modules.aoi.national_aoi import (
    get_region_aoi,
    get_aoi_bbox
)

print("===== RIMBARA CITY AOI TEST =====")

geometry = get_region_aoi(
    admin_code="51.71",
    allow_incomplete=False
)

print("\n===== RESULT =====")
print("Wilayah: Kota Denpasar")
print("Geometry:", geometry.geom_type)
print("Valid:", geometry.is_valid)
print("Area:", geometry.area)
print("BBOX:", get_aoi_bbox(geometry))

assert geometry.is_valid
assert not geometry.is_empty

print("\nCITY AOI TEST PASSED!")
