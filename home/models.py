from django.db import models
from django.utils.html import format_html
from django.utils.timezone import now

from common.utils.datetime import time_hour
from common.utils.image import thumbnail
from .managers import CityQuerySet, WeatherDayQuerySet

THUMBNAIL_SIZE = (400, 300)


class Country(models.Model):
    title = models.CharField(max_length=128, verbose_name="Название")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
        ordering = ("title",)


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name="Название")
    population = models.PositiveBigIntegerField(null=True, blank=True, verbose_name="Население")
    area = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Площадь")
    image = models.ImageField(null=True, blank=True, verbose_name="Изображение")
    image_small = models.ImageField(null=True, blank=True, verbose_name="Изображение, миниатюра")
    timezone = models.CharField(max_length=64, null=True, blank=True, verbose_name="Таймзона")

    def _population_mln(self):
        return self.population and round(self.population / 10**6, 1)
    _population_mln.short_description = "Население, млн. чел."
    population_mln = property(_population_mln)

    def _image_preview(self):
        if self.image_small:
            return format_html(f"""<img src="{self.image_small.url}" style="max-width: 70px">""")
        else:
            return "-"
    _image_preview.short_description = "Предпросмотр картинки"
    image_preview = property(_image_preview)

    objects = CityQuerySet.as_manager()

    @property
    def time_hour(self):
        return time_hour(now(), self.timezone or "UTC")

    def __str__(self):
        return f"{self.title}, {self.country.title}"

    def save(self, *args, **kwargs):
        if self.image and not self.image_small:
            self.image_small = thumbnail(self.image, size=THUMBNAIL_SIZE)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ("-population",)


class WeatherDay(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="weather")

    date_epoch = models.PositiveBigIntegerField("Время UNIX")
    date = models.DateField("День")

    maxtemp_c = models.FloatField("Max температура, °C")
    mintemp_c = models.FloatField("Min температура, °C")
    avgtemp_c = models.FloatField("Средняя температура, °C")
    maxwind_kph = models.FloatField("Max скорость вектра, км/ч")
    totalprecip_mm = models.FloatField("Осадки в течение дня, мм")
    avghumidity = models.PositiveSmallIntegerField("Средняя влажность, %")
    condition = models.JSONField("Условия")

    objects = WeatherDayQuerySet.as_manager()

    @property
    def is_future(self):
        return now().timestamp() < self.date_epoch


class Weather(models.Model):
    weather_day = models.ForeignKey(WeatherDay, null=True, on_delete=models.SET_NULL, related_name="hours")

    time_epoch = models.PositiveBigIntegerField("Время UNIX")
    time = models.DateTimeField("Время")

    temp_c = models.FloatField("Температура C")
    is_day = models.PositiveSmallIntegerField("Светлое время суток")
    condition = models.JSONField("Условия")
    wind_kph = models.FloatField("Ветер, км/ч")
    wind_degree = models.PositiveSmallIntegerField("Направление ветра, °")
    wind_dir = models.CharField("Направление ветра", max_length=16)
    pressure_in = models.FloatField("Давление, дюймы")
    precip_mm = models.PositiveSmallIntegerField("Осадки, мм")
    humidity = models.PositiveSmallIntegerField("Влажность, %")

    @property
    def is_future(self):
        return now().timestamp() < self.time_epoch

    @property
    def time_hour(self):
        return time_hour(self.time, self.weather_day.city.timezone)

    @property
    def wet_or_dry(self):
        return "wet" if self.humidity > 80 else "dry"


class Current(models.Model):
    city = models.OneToOneField(City, on_delete=models.CASCADE, primary_key=True, related_name="current")
    weather = models.ForeignKey(Weather, null=True, on_delete=models.SET_NULL, related_name="+")
    updated_at = models.DateTimeField(auto_now=True)
