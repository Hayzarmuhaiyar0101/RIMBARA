
import numpy as np

from modules.statistics import calculate_burn_statistics


severity = np.array([
    [4, 5, 6, 7]
])

result = calculate_burn_statistics(
    severity,
    pixel_size=20
)

print("\n===== RIMBARA BURN STATISTICS =====")

print("Total Pixels:", result["total_pixels"])

print(
    "Total Area:",
    result["total_area_hectares"],
    "hectares"
)

for name, data in result["classes"].items():

    if data["pixels"] > 0:

        print(
            name,
            "| Pixels:", data["pixels"],
            "| Area:", data["area_hectares"], "ha"
        )
