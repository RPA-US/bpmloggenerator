web: gunicorn agosuirpa.wsgi:application
cp configuration/ci-cd/heroku_settings.py agosuirpa/settings.py
python manage.py makemigrations
python manage.py migrate