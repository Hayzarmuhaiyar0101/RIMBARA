
from pystac_client import Client

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/"
COLLECTION = "sentinel-2-l2a"

def search_sentinel2(
    bbox,
    start_date,
    end_date,
    max_cloud=30,
    max_items=100
):
    """
    Mencari citra Sentinel-2 Level-2A.
    """

    catalog = Client.open(STAC_URL)

    search = catalog.search(
        collections=[COLLECTION],
        bbox=bbox,
        datetime=f"{start_date}T00:00:00Z/{end_date}T23:59:59Z",
        query={
            "eo:cloud_cover": {
                "lt": max_cloud
            }
        },
        max_items=max_items
    )

    items = list(search.items())

    items.sort(
        key=lambda item: item.properties.get(
            "eo:cloud_cover", 100
        )
    )

    print(f"Jumlah citra ditemukan: {len(items)}")

    for item in items:
        print(
            item.id,
            item.datetime,
            item.properties.get("eo:cloud_cover")
        )

    return items
