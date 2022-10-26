#!/bin/bash
/agosuirpa/venv/bin/python /agosuirpa/manage.py makemigrations
/agosuirpa/venv/bin/python /agosuirpa/manage.py makemigrations users
/agosuirpa/venv/bin/python /agosuirpa/manage.py makemigrations experiments
/agosuirpa/venv/bin/python /agosuirpa/manage.py makemigrations wizard
/agosuirpa/venv/bin/python /agosuirpa/manage.py migrate
/agosuirpa/venv/bin/python /agosuirpa/manage.py collectstatic --noinput
/agosuirpa/venv/bin/python -m gunicorn agosuirpa.wsgi:application -b 0.0.0.0:8000