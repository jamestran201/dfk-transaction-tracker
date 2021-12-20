.PHONY: install migrate-up runserver

install:
	poetry install

migrate-up:
	python dfk_transaction_tracker/manage.py migrate

runserver:
	python dfk_transaction_tracker/manage.py runserver