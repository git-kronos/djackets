init:
	pip install -U pip
	pip install -r requirements.txt

update-dependency:
	pip freeze > requirements.txt

run-insecure:
	python ./manage.py runserver --insecure

run:
	python ./manage.py runserver

deploy-check:
	python manage.py check --deploy

migrate:
	python manage.py makemigrations
	python manage.py migrate

createsuperuser:
	python manage.py createsuperuser --email admin@example.com --username admin

collect-static:
	python manage.py collectstatic

clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf