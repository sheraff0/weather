from django.core.management.base import BaseCommand

from home.assets import CITIES_DATA, image_file
from home.models import Country, City


class Command(BaseCommand):
    help = "Заполнение списка городов"

    def handle(self, *args, **options):
        for data in CITIES_DATA:
            city_title, country_title, image_title = map(data.get, ("city", "country", "image"))
            country_obj, _ = Country.objects.get_or_create(title=country_title)
            city_obj, _ = City.objects.get_or_create(title=city_title, country=country_obj)

            for key in ("population", "area"):
                value = int(data[key]) if data[key] else None
                setattr(city_obj, key, value)

            if image_title and not city_obj.image:
                city_obj.image = image_file(image_title)

            city_obj.save()
