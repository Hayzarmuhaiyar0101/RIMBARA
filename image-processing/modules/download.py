
import os
from pathlib import Path
from urllib.parse import urlparse

import boto3
from botocore.config import Config
from dotenv import load_dotenv


# Membaca konfigurasi dari .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def create_s3_client():

    access_key = os.getenv("CDSE_ACCESS_KEY")
    secret_key = os.getenv("CDSE_SECRET_KEY")

    if not access_key or not secret_key:
        raise ValueError(
            "Kredensial Copernicus belum dikonfigurasi."
        )

    return boto3.client(
        "s3",
        endpoint_url="https://eodata.dataspace.copernicus.eu",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="default",
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"}
        )
    )


def download_asset(s3_client, asset, output_path):

    parsed = urlparse(asset.href)

    if parsed.scheme != "s3":
        raise ValueError(
            f"Format aset tidak didukung: {asset.href}"
        )

    bucket = parsed.netloc
    key = parsed.path.lstrip("/")

    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if output_path.exists():
        print(f"File sudah tersedia: {output_path}")
        return str(output_path)

    print(f"\nMengunduh aset: {output_path.name}")

    s3_client.download_file(
        bucket,
        key,
        str(output_path)
    )

    print(f"Berhasil: {output_path}")

    return str(output_path)


def download_required_bands(item, output_dir):

    s3_client = create_s3_client()

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    required_assets = {
        "B08_10m": "B08_10m.jp2",
        "B12_20m": "B12_20m.jp2",
        "SCL_20m": "SCL_20m.jp2"
    }

    downloaded_files = {}

    for asset_key, filename in required_assets.items():

        if asset_key not in item.assets:
            raise KeyError(
                f"Aset tidak ditemukan: {asset_key}"
            )

        output_path = output_dir / filename

        downloaded_files[asset_key] = download_asset(
            s3_client,
            item.assets[asset_key],
            output_path
        )

    return downloaded_files
