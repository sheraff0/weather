#!/bin/bash

sleep 1s

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py fill_cities
python manage.py default_admin

if [ -z ${DEBUG} ];
then
  echo "Starting with Gunicorn"
  gunicorn weather.wsgi:application \
    -b 0.0.0.0:8000 --threads 2 \
    --workers 4 -k uvicorn.workers.UvicornWorker
else
  echo "Starting with Django dev server"
  ./manage.py runserver 0.0.0.0:8000
fi
