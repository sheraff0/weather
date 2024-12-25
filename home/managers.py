from datetime import timedelta
import random

from django.db.models import QuerySet, Prefetch, OuterRef, Subquery
from django.utils import timezone


class CityQuerySet(QuerySet):
    def exclude_empty_images(self):
        return self.exclude(
            image__in=[None, ""]
        )

    def list_with_related(self):
        return self.select_related(
            "country", "current__weather"
        ).exclude_empty_images()

    def item_with_related(self, pk):
        WeatherDay = self.model.weather.field.model
        Weather = WeatherDay.hours.field.model
        prefetch = WeatherDay.objects.filter(
            city_id=pk
        ).prefetch_related(
            Prefetch("hours", queryset=Weather.objects.order_by("time"))
        ).filter(
            date__gte=timezone.now().date()
        ).order_by("date")
        return self.prefetch_related(
            Prefetch("weather", queryset=prefetch)
        ).get(pk=pk)

    def random_choices(self, k: int = 5):
        ids = self.exclude_empty_images().values_list("pk", flat=True)
        return random.choices(ids, k=k)

    def random_choices_forecast(self, k: int = 5, grouped: bool = False):
        WeatherDay = self.model.weather.field.model
        ids = self.random_choices(k=k)
        qs = WeatherDay.objects.forecast(city_ids=ids)
        if grouped:
            res = {}
            for item in qs:
                city = f"{item.city.title} ({item.city.country})"
                res.setdefault(city, []).append(item)
            return [*res.items()]
        return qs


class WeatherDayQuerySet(QuerySet):
    def forecast(self, city_ids: list[int] = None):
        t0 = timezone.now()
        t1 = t0 + timedelta(days=3)
        cities_filter = {"city_id__in": city_ids} if city_ids else {}

        return self.filter(
            date__gte=t0.date(),
            date__lte=t1.date(),
            **cities_filter,
        ).select_related(
            "city__country"
        ).order_by("city__title", "date")
