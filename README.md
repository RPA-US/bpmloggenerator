# AGOSUIRPA
Automatic generation of synthetic UI log in RPA context introducing variability.

## Before run
You need to have [Python](https://www.python.org/downloads/) installed.

If desired, you can create an isolated installation of the project requirements by creating a [virtual environment](https://docs.python.org/3/library/venv.html#:~:text=A%20virtual%20environment%20is%20a,part%20of%20your%20operating%20system.).

## Configuration DB
Firstly, you need configure the Database for the proyect. To do this, create an *.env* file in the folder *configuration* with the following contents:
`
-  DB_NAME="Database name"
-  DB_HOST="Database URL"
-  DB_PORT="Database access port"
-  DB_USER="Database user to access. Use a new user with limited credentials"
-  DB_PASSWORD="Password for the previous user"
-  DJANGO_SETTINGS_MODULE=agosuirpa.settings
-  DJANGO_SECRET_KEY="Secret text for cryptographic purposes"
`
## Project initialization

In the project directory, open a terminal and run:

**`python manage.py makemigrations`**

To create a DB model.

**`python manage.py migrate`**

To create the tables in the DB based on project models.

**`python manage.py loaddata configuration/db_populate.json`**

To insert initial data in DB.

**`python manage.py runserver`**

Runs the app in the debug mode. If you want to init in deploy mode, change in the *agosuirpa/settings.py* file, the *DEBUG* mode attribute to False.

## Learn More

You can learn more about the deploy of the aplication backend in the [Django documentation](https://docs.djangoproject.com/en/4.0/).

A video demo is available at: [AGOSUIRPA](https://youtu.be/RrrNs2wczos)
