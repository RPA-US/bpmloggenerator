release: rm agosuirpa/settings.py &&  cp configuration/ci-cd/heroku_settings.py agosuirpa/settings.py && python manage.py makemigrations && python manage.py migrate
web: gunicorn agosuirpa.wsgi:application
