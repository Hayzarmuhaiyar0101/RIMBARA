
import numpy as np


def calculate_dnbr(nbr_pre, nbr_post):

    nbr_pre = np.asarray(nbr_pre, dtype=np.float32)
    nbr_post = np.asarray(nbr_post, dtype=np.float32)

    if nbr_pre.shape != nbr_post.shape:
        raise ValueError("Ukuran citra tidak sama!")

    valid = (
        np.isfinite(nbr_pre) &
        np.isfinite(nbr_post)
    )

    result = np.full(
        nbr_pre.shape,
        np.nan,
        dtype=np.float32
    )

    result[valid] = nbr_pre[valid] - nbr_post[valid]

    return result
