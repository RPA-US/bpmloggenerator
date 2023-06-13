#!/bin/bash
/bpmloggenerator/venv/bin/python /bpmloggenerator/manage.py makemigrations
/bpmloggenerator/venv/bin/python /bpmloggenerator/manage.py makemigrations users
/bpmloggenerator/venv/bin/python /bpmloggenerator/manage.py makemigrations experiments
/bpmloggenerator/venv/bin/python /bpmloggenerator/manage.py makemigrations wizard
/bpmloggenerator/venv/bin/python /bpmloggenerator/manage.py migrate
/bpmloggenerator/venv/bin/python /bpmloggenerator/manage.py collectstatic --noinput
/bpmloggenerator/venv/bin/python -m gunicorn bpmloggenerator.wsgi:application -b 0.0.0.0:8000