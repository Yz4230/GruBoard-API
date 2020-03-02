freeze:
	pip freeze > reqs.txt

migrate:
	python manage.py migrate

mkmigs:
	python manage.py makemigrations
