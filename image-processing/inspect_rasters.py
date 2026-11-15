
import rasterio
import numpy as np
from pathlib import Path

PRODUCT_ID = (
    "S2C_MSIL2A_20260320T022531_"
    "N0512_R046_T49MHU_20260320T061512"
)

DATA_DIR = (
    Path("data")
    / "raw"
    / "post_fire"
    / PRODUCT_ID
)

BANDS = {
    "NIR": "B08_10m.jp2",
    "SWIR": "B12_20m.jp2",
    "SCL": "SCL_20m.jp2"
}


def inspect_raster(name, filename):

    path = DATA_DIR / filename

    print(f"\n===== {name} =====")

    if not path.exists():
        print("FILE TIDAK DITEMUKAN!")
        return None

    with rasterio.open(path) as src:

        data = src.read(1)

        print("File       :", filename)
        print("Driver     :", src.driver)
        print("Width      :", src.width)
        print("Height     :", src.height)
        print("CRS        :", src.crs)
        print("Resolution :", src.res)
        print("Bounds     :", src.bounds)
        print("NoData     :", src.nodata)
        print("Data type  :", src.dtypes[0])

        valid = np.isfinite(data)

        if src.nodata is not None:
            if not np.isnan(src.nodata):
                valid &= data != src.nodata

        if np.any(valid):

            print("Min value  :", float(data[valid].min()))
            print("Max value  :", float(data[valid].max()))
            print("Mean value :", float(data[valid].mean()))

        else:
            print("Tidak ada piksel valid!")

        return {
            "crs": src.crs,
            "transform": src.transform,
            "width": src.width,
            "height": src.height,
            "bounds": src.bounds,
            "resolution": src.res
        }


def main():

    print("===== RIMBARA RASTER VALIDATION =====")

    results = {}

    for name, filename in BANDS.items():

        results[name] = inspect_raster(
            name,
            filename
        )

    print("\n===== GRID VALIDATION =====")

    if not all(results.values()):
        print("Validasi gagal: ada raster yang tidak terbaca.")
        return

    nir = results["NIR"]
    swir = results["SWIR"]
    scl = results["SCL"]

    same_swir_scl = (
        swir["crs"] == scl["crs"]
        and swir["transform"] == scl["transform"]
        and swir["width"] == scl["width"]
        and swir["height"] == scl["height"]
    )

    same_nir_swir = (
        nir["crs"] == swir["crs"]
        and nir["transform"] == swir["transform"]
        and nir["width"] == swir["width"]
        and nir["height"] == swir["height"]
    )

    print("B12 dan SCL satu grid:", same_swir_scl)
    print("B08 dan B12 satu grid:", same_nir_swir)

    print("\nRASTER VALIDATION COMPLETED!")


if __name__ == "__main__":
    main()
