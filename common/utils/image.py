from io import BytesIO
from PIL import Image
import re

from django.core.files.images import ImageFile
from django.db import models


def thumbnail(
    image: models.ImageField,
    size: tuple[int, int],
    quality: int = 80
):
    filename, ext = re.match(r"^(.*)\.(\w+)$", image.name).groups()
    im = Image.open(image)
    im.thumbnail(size=size)
    output = BytesIO()
    im.save(output, format=ext.upper(), quality=quality)

    return ImageFile(output, name=f"{filename}.small.{ext}")
