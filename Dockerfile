FROM python:3.13-slim-bullseye

RUN apt update && apt install -y gcc libmagickwand-dev

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ADD . /app

WORKDIR /app
