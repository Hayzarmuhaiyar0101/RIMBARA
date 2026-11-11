
import numpy as np


CLASS_NAMES = {
    1: "Regenerasi tinggi",
    2: "Regenerasi rendah",
    3: "Tidak terbakar / perubahan rendah",
    4: "Keparahan rendah",
    5: "Keparahan sedang-rendah",
    6: "Keparahan sedang-tinggi",
    7: "Keparahan tinggi"
}


def classify_burn_severity(dnbr):

    result = np.zeros(dnbr.shape, dtype=np.uint8)

    valid = np.isfinite(dnbr)

    result[valid & (dnbr < -0.25)] = 1
    result[valid & (dnbr >= -0.25) & (dnbr < -0.10)] = 2
    result[valid & (dnbr >= -0.10) & (dnbr <= 0.10)] = 3
    result[valid & (dnbr > 0.10) & (dnbr <= 0.27)] = 4
    result[valid & (dnbr > 0.27) & (dnbr <= 0.44)] = 5
    result[valid & (dnbr > 0.44) & (dnbr <= 0.66)] = 6
    result[valid & (dnbr > 0.66)] = 7

    return result
    