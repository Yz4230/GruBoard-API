freeze:
	pip freeze > requirements.txt

migrate:
	python manage.py migrate

mkmigs:
	python manage.py makemigrations gruboard_api

run:
	python manage.py runserver 0.0.0.0:8000

start:
	make mkmigs
	make migrate
	make run