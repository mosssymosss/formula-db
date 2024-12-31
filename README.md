# formula-db

Run this command

    pip install -r requirements.txt



You need to have a file called .env that has your configurations, i.e.

    POSTGRES_ADMIN_USER={admin_username} # username with privileges to create new users and databases
    POSTGRES_ADMIN_PASSWORD={admin_username_password}
    POSTGRES_DB={your_db_name}
    POSTGRES_HOST={your_host}
    POSTGRES_PORT={your_port}
    POSTGRES_CURRENT_USER={your_user} # username that will be using the created database, if it doesnt exist it will be created
    POSTGRES_CURRENT_USER_PASSWORD={your_user_password}

    DATABASE_URL=postgresql://${POSTGRES_CURRENT_USER}:${POSTGRES_CURRENT_USER_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

    API_BASE_URL="http://127.0.0.1:8000"

Alembic relies on the DATABASE_URL



Run the init.db file to make the database and it's tables


Apply all migration by running this

    alembig upgrade head




While in the directpry of the project, run 

    uvicorn app.main:app --reload

then open you browser and go to

    API_BASE_URL/home

you will have access to the full ui




Run the populate_db_random.py to populate the database with random data

It takes command line arguments to specify the number of drivers, circuits and races it should generate

By default driver=5000, circuits=5000, races=50000

It also takes as an argument which of the tables it should generate, by default all of them are generated

The races table depend on the drivers and circuits table, make sure they exist when generating only the races table



Run this to see how to use populate_bd_random.py

    python populate_db_random.py --help


