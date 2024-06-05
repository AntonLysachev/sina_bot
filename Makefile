install:
	poetry install

start:
	poetry run python app.py

lint:
	poetry run flake8 bot

test:
	poetry run  pytest --cov=bot
