
import matplotlib.pyplot as plt
import numpy as np


def visualize_dnbr(dnbr, output_path):

    plt.figure(figsize=(10, 6))

    image = plt.imshow(
        dnbr,
        cmap="RdYlGn_r",
        vmin=-0.25,
        vmax=1.0
    )

    plt.colorbar(
        image,
        label="dNBR Value"
    )

    plt.title("RIMBARA - Burn Severity Analysis")
    plt.xlabel("Pixel X")
    plt.ylabel("Pixel Y")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.show()

    print(f"Peta dNBR berhasil disimpan: {output_path}")
