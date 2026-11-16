
from config.analysis_config import AnalysisConfig

config = AnalysisConfig()

print("===== RIMBARA NATIONAL CONFIGURATION =====")

try:

    config.validate()

    print("Configuration: VALID")

    for key, value in config.summary().items():
        print(f"{key}: {value}")

    print("\nNATIONAL CONFIGURATION ONLINE!")

except ValueError as error:

    print("CONFIGURATION ERROR:", error)
