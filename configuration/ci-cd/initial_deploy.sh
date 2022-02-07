#!/bin/sh
\cp -r configuration/ci-cd/heroku_settings.py agosuirpa/settings.py 
python agosuirpa/manage.py makemigrations 
python agosuirpa/manage.py migrate
