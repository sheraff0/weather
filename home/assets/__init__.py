import csv
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.files.images import ImageFile

ASSETS_DIR = Path(settings.BASE_DIR) / "home/assets"


def read_from_csv(filename):
    with open(ASSETS_DIR / filename) as f:
        reader = csv.DictReader(f)
        data = [*reader]
        return data


def image_file(filename, path: str = "city_images"):
    with open(ASSETS_DIR / path / filename, "rb") as f:
        buffer = BytesIO(f.read())
        return ImageFile(buffer, name=filename)


CITIES_DATA = read_from_csv("cities.csv")
