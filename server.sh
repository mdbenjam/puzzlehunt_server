#!/bin/bash
python3 ./manage.py collectstatic --noinput
python3 ./manage.py loaddata initial_hunt
python3 ./manage.py migrate --no-input
gunicorn --workers=5 --bind=0.0.0.0:8000 puzzlehunt_server.wsgi:application