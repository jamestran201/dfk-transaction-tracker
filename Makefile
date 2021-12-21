.PHONY: install migrate-up runserver start-celery

install:
	poetry install

migrate-up:
	python manage.py migrate

runserver:
	python manage.py runserver

start-celery:
	celery -A dfk_transaction_tracker worker -l INFO
