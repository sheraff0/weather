from datetime import date
import requests

from django.conf import settings


class WeatherApiClient:
    BASE_URL = "http://api.weatherapi.com/v1"
    API_KEY = settings.WEATHER_API_KEY
    lang = "ru"

    @classmethod
    def get(cls, endpoint, q, **kwargs):
        r = requests.get(f"{cls.BASE_URL}/{endpoint}", params=dict(
            q=q, lang=cls.lang, key=cls.API_KEY, **kwargs))
        return r.json()

    @classmethod
    def current(cls, q):
        return cls.get("current.json", q)

    @classmethod
    def forecast(cls, q, days: int = 3):
        return cls.get("forecast.json", q, days=days)

    @classmethod
    def history(cls, q, dt: date = "2024-01-01"):
        return cls.get("history.json", q, dt=dt)

    @classmethod
    def location(cls, q):
        return cls.get("timezone.json", q)
