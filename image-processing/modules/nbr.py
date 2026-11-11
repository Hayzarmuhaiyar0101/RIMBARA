
import numpy as np


def calculate_nbr(nir, swir):
    nir = np.asarray(nir, dtype=np.float32)
    swir = np.asarray(swir, dtype=np.float32)

    denominator = nir + swir

    valid = (
        np.isfinite(nir) &
        np.isfinite(swir) &
        (denominator != 0)
    )

    result = np.full(nir.shape, np.nan, dtype=np.float32)

    result[valid] = (
        (nir[valid] - swir[valid]) /
        denominator[valid]
    )

    return result
