
import requests

SOURCES = {
    "BIG BATAS_WILAYAH - Layer 13": (
        "https://geoservices.big.go.id/rbi/rest/services/"
        "BATASWILAYAH/BATAS_WILAYAH/MapServer/13"
    ),
    "BIG RBI 50K - Layer 0": (
        "https://kspservices.big.go.id/satupeta/rest/services/"
        "RBI/Administrasi_AR_KabKota_50K/MapServer/0"
    )
}


def diagnose(name, base_url):

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    try:
        metadata_response = requests.get(
            base_url,
            params={"f": "pjson"},
            timeout=90
        )
        metadata_response.raise_for_status()

        metadata = metadata_response.json()

        if "error" in metadata:
            print("METADATA ERROR:", metadata["error"])
            return

        print("Layer name:", metadata.get("name"))
        print("Geometry:", metadata.get("geometryType"))
        print("Display field:", metadata.get("displayField"))
        print("Max records:", metadata.get("maxRecordCount"))
        print("Description:", metadata.get("description"))
        print("Extent:", metadata.get("extent"))

        print("\nDAFTAR FIELD:")

        for field in metadata.get("fields", []):
            print(
                field.get("name"),
                "|",
                field.get("type"),
                "|",
                field.get("alias")
            )

        query_url = base_url + "/query"

        response = requests.get(
            query_url,
            params={
                "where": "1=1",
                "outFields": "*",
                "returnGeometry": "false",
                "resultRecordCount": 3,
                "orderByFields": "OBJECTID ASC",
                "f": "json"
            },
            timeout=90
        )

        response.raise_for_status()

        result = response.json()

        if "error" in result:
            print("QUERY ERROR:", result["error"])
            return

        print("\nCONTOH ATRIBUT:")

        for feature in result.get("features", []):
            print(feature.get("attributes", {}))

        print("\nVALIDATION: SUCCESS")

    except Exception as error:
        print("VALIDATION FAILED:", error)


if __name__ == "__main__":

    for name, url in SOURCES.items():
        diagnose(name, url)

    print("\n===== BOUNDARY SOURCE DIAGNOSTIC COMPLETED =====")
