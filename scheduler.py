from concurrent.futures import ThreadPoolExecutor
import time

import django
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from apscheduler.schedulers.background import BackgroundScheduler

from home.models import City
from home.services import update_weather_for_city

scheduler = BackgroundScheduler()
HEADER = "\n\n\n---=== WEATHER APP SCHEDULER ===---\n"


def _update_weather_for_city(city):
    if update_weather_for_city(city):
        print(f"-= Updating weather for {city} =-", flush=True)


@scheduler.scheduled_job("cron", minute="*/5")
def update_weather_job():
    qs = City.objects.list_with_related()
    cities = [*qs]

    print(HEADER)
    print("...Синхронизация с сервисом WeatherAPI...", flush=True)
    with ThreadPoolExecutor(max_workers=5) as pool:
        pool.map(_update_weather_for_city, cities)


@scheduler.scheduled_job("cron", minute="*")
# @scheduler.scheduled_job("cron", minute="*/15")
def mailing_list():
    qs = get_user_model().extra.mailing_list()
    emails = [*qs.values_list("email", flat=True)]

    print(HEADER)
    print("...Рассылка email по подписке...", flush=True)
    random_choices_forecast = City.objects.random_choices_forecast(grouped=True)
    print([(city, [(x.date, x.avgtemp_c) for x in items])
           for city, items in random_choices_forecast], flush=True)
    print(emails, flush=True)
    # send_mail("Погода в мире", )

if __name__ == "__main__":
    try:
        scheduler.start()
        while True:
            print(HEADER, flush=True)
            print(scheduler.print_jobs(), flush=True)
            time.sleep(60)
    finally:
        scheduler.shutdown(wait=False)