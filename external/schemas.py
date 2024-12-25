from datetime import date

from pydantic import BaseModel, NaiveDatetime, Field


class Location(BaseModel):
    name: str
    region: str
    country: str
    lat: float
    lon: float
    tz_id: str
    localtime_epoch: int
    localtime: NaiveDatetime


class Condition(BaseModel):
    text: str
    icon: str
    code: int


class CommonDataMixin:
    temp_c: float
    is_day: int
    condition: Condition
    wind_kph: float
    wind_degree: int
    wind_dir: str
    pressure_in: float
    precip_mm: float
    humidity: int


class Current(CommonDataMixin, BaseModel):
    time_epoch: int = Field(..., validation_alias="last_updated_epoch")
    time: NaiveDatetime = Field(..., validation_alias="last_updated")


class ForecastHour(CommonDataMixin, BaseModel):
    time_epoch: int
    time: NaiveDatetime


class ForecastDay(BaseModel):
    maxtemp_c: float
    mintemp_c: float
    avgtemp_c: float
    maxwind_kph: float
    totalprecip_mm: float
    avghumidity: int
    condition: Condition


class ForecastDayItem(BaseModel):
    date: date
    date_epoch: int
    day: ForecastDay
    hour: list[ForecastHour]


class Forecast(BaseModel):
    forecastday: list[ForecastDayItem]


class ForecastResponse(BaseModel):
    location: Location
    current: Current
    forecast: Forecast


class HistoryResponse(BaseModel):
    location: Location
    forecast: Forecast
