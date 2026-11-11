
import rasterio
import numpy as np


def save_geotiff(output_path, data, profile, dtype=None):

    output_profile = profile.copy()

    output_profile.update(
        driver="GTiff",
        count=1,
        compress="lzw",
        nodata=-9999
    )

    if dtype is not None:
        output_profile.update(dtype=dtype)
    else:
        output_profile.update(dtype="float32")

    output = np.where(
        np.isfinite(data),
        data,
        -9999
    )

    with rasterio.open(output_path, "w", **output_profile) as dst:
        dst.write(output.astype(output_profile["dtype"]), 1)

    print(f"File berhasil disimpan: {output_path}")
