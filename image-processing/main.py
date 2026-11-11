
import numpy as np

from modules.nbr import calculate_nbr
from modules.dnbr import calculate_dnbr
from modules.classification import classify_burn_severity
from modules.visualization import visualize_dnbr


def run_rimbara():

    # Simulasi data untuk pengujian mesin
    nir_pre = np.array([[0.75, 0.70, 0.65, 0.60]])
    swir_pre = np.array([[0.15, 0.20, 0.25, 0.30]])

    nir_post = np.array([[0.70, 0.55, 0.35, 0.20]])
    swir_post = np.array([[0.20, 0.35, 0.45, 0.55]])

    # NBR
    nbr_pre = calculate_nbr(nir_pre, swir_pre)
    nbr_post = calculate_nbr(nir_post, swir_post)

    # dNBR
    dnbr = calculate_dnbr(nbr_pre, nbr_post)

    # Classification
    severity = classify_burn_severity(dnbr)
    visualize_dnbr(dnbr, "outputs/dnbr_simulation.png")


    print("\n===== RIMBARA IMAGE PROCESSING =====")
    print("NBR Before:", nbr_pre)
    print("NBR After :", nbr_post)
    print("dNBR      :", dnbr)
    print("Severity  :", severity)

    print("\nRIMBARA PROCESS COMPLETED!")


if __name__ == "__main__":
    run_rimbara()
