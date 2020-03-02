freeze:
	pip freeze > requirements.txt

migrate:
	python manage.py migrate

mkmigs:
	python manage.py makemigrations
