
from modules.aoi.national_aoi import (
    get_province_aoi,
    get_aoi_bbox
)

print("===== RIMBARA PROVINCE AOI TEST =====")

province = "Bali"

geometry = get_province_aoi(
    province=province,
    allow_incomplete=False
)

print("\n===== RESULT =====")
print("Province:", province)
print("Geometry:", geometry.geom_type)
print("Valid:", geometry.is_valid)
print("Area:", geometry.area)
print("BBOX:", get_aoi_bbox(geometry))

assert geometry.is_valid
assert not geometry.is_empty

print("\nPROVINCE AOI TEST PASSED!")
