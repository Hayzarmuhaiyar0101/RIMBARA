
import rasterio
import numpy as np
from pathlib import Path

PRODUCT_ID = (
    "S2C_MSIL2A_20260320T022531_"
    "N0512_R046_T49MHU_20260320T061512"
)

path = (
    Path("data/raw/post_fire")
    / PRODUCT_ID
    / "SCL_20m.jp2"
)

print("===== RIMBARA SCL FULL RESOLUTION DIAGNOSTIC =====")

# PENTING:
# Abaikan internal JP2 overviews
with rasterio.open(
    path,
    OVERVIEW_LEVEL="NONE"
) as src:

    data = src.read(1)

    print("CRS:", src.crs)
    print("Shape:", data.shape)
    print("Resolution:", src.res)
    print("Data type:", data.dtype)

    values, counts = np.unique(
        data,
        return_counts=True
    )

    print("\n===== FULL RESOLUTION SCL VALUES =====")

    for value, count in zip(values, counts):

        percentage = count / data.size * 100

        print(
            f"Class {value}: "
            f"{count:,} pixels "
            f"({percentage:.2f}%)"
        )

    valid_classes = set(range(12))
    actual_classes = set(values.tolist())

    unexpected = actual_classes - valid_classes

    print("\n===== VALIDATION =====")

    print("Unexpected classes:", unexpected)

    if unexpected:
        print("WARNING: Ada nilai di luar kelas SCL.")
    else:
        print("SCL CLASS VALUES VALID!")

print("\n===== SCL FILE INVESTIGATION =====")

print("File size (bytes):", path.stat().st_size)
print("File size (MB):", round(
    path.stat().st_size / (1024 * 1024), 4
))

with rasterio.open(
    path,
    OVERVIEW_LEVEL="NONE"
) as src:

    print("Driver:", src.driver)
    print("Image structure:", src.tags(
        ns="IMAGE_STRUCTURE"
    ))
    print("Overviews:", src.overviews(1))
    print("Band tags:", src.tags(1))

    print("Sample pixels:")
    print(src.read(
        1,
        window=((0, 10), (0, 10))
    ))

print("\nDIAGNOSTIC COMPLETED!")
