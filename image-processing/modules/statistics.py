
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


def calculate_burn_statistics(
    severity,
    pixel_size=20
):
    """
    Menghitung luas setiap kelas dalam hektare.
    pixel_size menggunakan satuan meter.
    """

    pixel_area = (pixel_size * pixel_size) / 10000

    valid = severity > 0

    total_pixels = int(np.sum(valid))

    statistics = {}

    for class_id, class_name in CLASS_NAMES.items():

        count = int(np.sum(severity == class_id))

        area = count * pixel_area

        statistics[class_name] = {
            "pixels": count,
            "area_hectares": round(area, 4)
        }

    total_area = total_pixels * pixel_area

    return {
        "total_pixels": total_pixels,
        "total_area_hectares": round(total_area, 4),
        "classes": statistics
    }
