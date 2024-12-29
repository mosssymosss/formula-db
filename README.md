# formula-db

Run this command

    pip install -r requirements.txt

You need to have a .env file that has your postgres configurations, i.e.

    POSTGRES_ADMIN_USER={admin_username} // username with privileges to create new users and databases
    POSTGRES_ADMIN_PASSWORD={admin_username_password}
    POSTGRES_DB={your_db_name}
    POSTGRES_HOST={your_host}
    POSTGRES_PORT={your_port}
    POSTGRES_CURRENT_USER={your_user} // username that will be using the created database
    POSTGRES_CURRENT_USER_PASSWORD={your_user_password}

    DATABASE_URL=postgresql://${POSTGRES_CURRENT_USER}:${POSTGRES_CURRENT_USER_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

    API_BASE_URL="http://127.0.0.1:8000"

Alembic relies on the DATABASE_URL

Run the init.db file to make the database and it's tables

Run alembic migrations

Run the populate_db_random.py to populate the database with random data
It takes command line arguments to specify the number of drivers, circuits and races it should generate
By default driver=5000, circuits=5000, races=50000
It also takes as an argument which of the tables it should generate, by default all of them are generated
The races table depend on the drivers and circuits table, make sure they exist when generating only the races table

Run this to see how to use populate_bd_random.py

    python populate_db_random.py --help





