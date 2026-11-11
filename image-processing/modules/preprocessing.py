
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling


def read_raster(path):
    """Membaca citra raster GeoTIFF."""

    with rasterio.open(path) as src:
        data = src.read(1).astype(np.float32)
        profile = src.profile.copy()
        nodata = src.nodata

    if nodata is not None:
        data[data == nodata] = np.nan

    return data, profile


def align_band_to_reference(source_path, reference_path):
    """Menyamakan grid dan resolusi citra."""

    with rasterio.open(reference_path) as ref:

        destination = np.full(
            (ref.height, ref.width),
            np.nan,
            dtype=np.float32
        )

        with rasterio.open(source_path) as src:
            reproject(
                source=rasterio.band(src, 1),
                destination=destination,
                src_transform=src.transform,
                src_crs=src.crs,
                src_nodata=src.nodata,
                dst_transform=ref.transform,
                dst_crs=ref.crs,
                dst_nodata=np.nan,
                resampling=Resampling.bilinear
            )

        profile = ref.profile.copy()

    return destination, profile


def apply_scl_mask(band, scl):
    """Menghilangkan awan dan gangguan citra Sentinel-2."""

    invalid_classes = [0, 1, 3, 8, 9, 10, 11]

    result = band.astype(np.float32).copy()

    mask = np.isin(scl, invalid_classes)

    result[mask] = np.nan

    return result
