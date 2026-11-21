
import requests
import time

API_URL = (
    "https://geoservices.big.go.id/rbi/rest/services/"
    "BATASWILAYAH/BATAS_WILAYAH/MapServer/13/query"
)

def main():

    print("===== RIMBARA SEQUENTIAL GEOMETRY TEST =====")

    for object_id in [1, 2]:

        print(f"\nMengambil OBJECTID: {object_id}")

        params = {
            "where": f"objectid = {object_id}",
            "outFields": "*",
            "returnGeometry": "true",
            "outSR": 4326,
            "f": "json"
        }

        try:

            response = requests.get(
                API_URL,
                params=params,
                timeout=(30, 180)
            )

            print("HTTP:", response.status_code)

            response.raise_for_status()

            data = response.json()

            if "error" in data:
                print("API ERROR:", data["error"])
                continue

            features = data.get("features", [])

            if features:

                feature = features[0]
                geometry = feature.get("geometry") or {}

                print("OBJECTID:", object_id)
                print("Nama:", feature["attributes"].get("namobj"))
                print("Polygon:", bool(geometry.get("rings")))
                print("Jumlah rings:", len(geometry.get("rings", [])))
                print("STATUS: SUCCESS")

            else:
                print("STATUS: NO FEATURE")

        except Exception as error:

            print("STATUS: FAILED")
            print("ERROR:", error)

        time.sleep(5)

    print("\n===== TEST COMPLETED =====")


if __name__ == "__main__":
    main()
