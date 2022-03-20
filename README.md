# AGOSUIRPA
Automatic generation of sintetic UI log in RPA context introducing variability

# Generate log
The software will generate a log with the characteristics defined in the screen of the second form for log generation.

To start using the platform, configure your postgresql database and set a .env file on 'agosuirpa/.env' with its information as follows:

```
DB_NAME=************
DB_HOST=************
DB_PORT=************
DB_USER=************
DB_PASSWORD=********
```

Then run the following commands:

```
python -m venv env
source env/Scripts/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```

# Analyzer
To use MELRPA analyzer module you have to run the platform as:
```
python manage.py runserver --noreload
```