
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class AnalysisConfig:

    # Identitas analisis
    region_name: str = "Indonesia"
    analysis_mode: str = "national"

    # Area pencarian (opsional)
    bbox: Optional[tuple] = None

    # Periode pencarian citra
    start_date: str = "2024-01-01"
    end_date: str = "2026-12-31"

    # Kualitas citra
    max_cloud: float = 30.0
    max_items: int = 100

    def validate(self):

        if self.analysis_mode not in ["national", "regional", "custom"]:
            raise ValueError("Mode analisis tidak valid.")

        start = date.fromisoformat(self.start_date)
        end = date.fromisoformat(self.end_date)

        if start > end:
            raise ValueError(
                "Tanggal mulai tidak boleh melebihi tanggal selesai."
            )

        if not 0 <= self.max_cloud <= 100:
            raise ValueError(
                "Batas tutupan awan harus 0 sampai 100."
            )

        if self.max_items < 1:
            raise ValueError(
                "Jumlah maksimum citra minimal 1."
            )

        if self.bbox is not None:

            if len(self.bbox) != 4:
                raise ValueError("BBOX harus memiliki 4 koordinat.")

            west, south, east, north = self.bbox

            if not (
                -180 <= west < east <= 180
                and -90 <= south < north <= 90
            ):
                raise ValueError("Koordinat BBOX tidak valid.")

        if self.analysis_mode == "custom" and self.bbox is None:
            raise ValueError(
                "Mode custom membutuhkan BBOX."
            )

        return True

    def summary(self):

        self.validate()

        return {
            "region": self.region_name,
            "mode": self.analysis_mode,
            "bbox": self.bbox,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "max_cloud": self.max_cloud,
            "max_items": self.max_items
        }
