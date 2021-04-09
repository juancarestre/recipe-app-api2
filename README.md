# recipe-app-api2
Recipe app api source code - Version 2
docker-compose run app sh -c "django-admin.py startproject app ."

python -m venv .venv/
chmod u+x .venv/bin/activate
source .venv/bin/activate
pip install -r requirements.txt

to run test

docker-compose run app sh -c "python manage.py test && flake8"
./run-test.sh


docker-compose run app sh -c "python manage.py startapp core"

docker-compose run app sh -c "python manage.py makemigrations core"