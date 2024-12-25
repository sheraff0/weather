from datetime import datetime, timedelta
from pytz import timezone as py_tz

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from external.client import WeatherApiClient
from external.schemas import ForecastResponse, ForecastDay, ForecastHour
from home.models import City, WeatherDay, Weather, Current
from weather.settings import UPDATE_INTERVAL

UPDATE_INTERVAL = timedelta(seconds=settings.UPDATE_INTERVAL)


class WeatherService:
    def __init__(self, city):
        self.city = city
        self.q = f"{self.city.title} {self.city.country.title}"
        self.client = WeatherApiClient()
        self.data = None
        self.timezone = None

    @property
    def needs_update(self):
        if hasattr(self.city, "current"):
            return self.city.current.updated_at + UPDATE_INTERVAL < timezone.now()
        return True

    def fetch(self):
        res = self.client.forecast(self.q)
        self.data = ForecastResponse.model_validate(res)
        self.timezone = self.data.location.tz_id

    def save_city(self):
        if self.city.timezone is None:
            self.city.timezone = self.timezone
            self.city.save()

    def tz_aware(self, time_epoch):
        return datetime.fromtimestamp(time_epoch).astimezone(py_tz(self.timezone))

    @transaction.atomic
    def save_current(self):
        attrs = self.data.current.model_dump()
        attrs["time"] = self.tz_aware(attrs["time_epoch"])
        current, _ = Current.objects.get_or_create(city=self.city)
        current.weather and current.weather.delete()
        weather = Weather.objects.create(**attrs)
        current.weather = weather
        current.save()

    def save_forecast(self):
        for data in self.data.forecast.forecastday:
            self.save_forecast_day(data)

    @transaction.atomic
    def save_forecast_day(self, data: ForecastDay):
        attrs = data.model_dump()
        date, day, hours = map(attrs.pop, ("date", "day", "hour"))
        attrs.update(day)

        weather_day, _ = WeatherDay.objects.update_or_create(
            city=self.city, date=date, defaults=attrs)

        for hour in hours:
            self.save_forecast_hour(weather_day, hour)

    def save_forecast_hour(self, weather_day: WeatherDay, attrs: dict):
        time_epoch = attrs.pop("time_epoch")
        attrs["time"] = self.tz_aware(time_epoch)
        Weather.objects.update_or_create(
            weather_day=weather_day, time_epoch=time_epoch, defaults=attrs)

    def save(self):
        self.save_city()
        self.save_current()
        self.save_forecast()


def update_weather_for_city(city):
    service = WeatherService(city)
    if service.needs_update:
        service.fetch()
        service.save()
        return True
    return False
