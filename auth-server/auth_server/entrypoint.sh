#!/bin/sh

python manage.py makemigrations accounts
python manage.py migrate accounts
python manage.py makemigrations
python manage.py migrate
python data_generator.py
python manage.py loaddata fixtures/player.json --app accounts.player
python manage.py loaddata fixtures/application.json --app oauth2_provider.application
python manage.py runserver ${AUTH_SERVER_WEB_ADDRESS}:${AUTH_SERVER_WEB_PORT}
exec "$@"
