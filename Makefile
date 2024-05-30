install:
	poetry install --no-root

PORT ?= 8000
start:
	poetry run python app.py

lint:
	poetry run flake8 bot

