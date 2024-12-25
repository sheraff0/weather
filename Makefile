.DEFAULT_GOAL := help
include .env

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

DC = docker compose
EXEC = docker exec

build:
	$(DC) build $(c)

up:
	$(DC) up $(c)

down:
	$(DC) down $(c)

su:
	$(DC) run --rm web ./manage.py createsuperuser

makemigrations:
	$(DC) run --rm web ./manage.py makemigrations

migrate:
	$(DC) run --rm web ./manage.py migrate

psql:
	$(EXEC) -it $(PROJECT_PREFIX)_db psql -U $(DB_USER) $(DB_NAME)
