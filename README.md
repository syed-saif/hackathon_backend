# Hackathon-backend-repo

**Steps to run the app**

1. Clone this repo
2. Open the terminal and create ``` virtualenv  ``` for this repo

```
virtualenv venv_ha
```

3. browse to the repo directory
4. Create Postgresql database - Login to the postgres shell and run this command:

```
create database hackathon_app;
```

5. Create ``` .env ``` file and add database name, username and password. Sample:

```
DATABASE_NAME='hackathon_app'
DATABASE_USERNAME='psqluser'
DATABASE_PASSWORD='psqlpassword'
```

6. Activate virutalenvironment

```
source </path/to/venv_ma>/bin/activate
```

7. Run ``` pip install -r requirements.txt ```. This should install all the dependecies.

8. Run migrations

```
python manage.py migrate
```

9. Run ``` python manage.py runserver ```. This should start the webserver and you are good to go.