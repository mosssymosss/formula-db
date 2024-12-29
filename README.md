# formula-db

Run this command

    pip install -r requirements.txt

You need to have a .env file that has your postgres configurations, i.e.

    POSTGRES_USER={your_username}
    POSTGRES_PASSWORD={your_password}
    POSTGRES_DB={your_database_name}
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432

    API_BASE_URL={your_base_url}

    DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}


Alembic relies on this last parameters

Run the init.db file to make the database and it's tables

Run alembic migrations

Run the populate_db_random.py to populate the database with random data
It takes command line arguments to specify the number of drivers, circuits and races it should generate
By default driver=5000, circuits=5000, races=50000
It also takes as an argument which of the tables it should generate, by default all of them are generated
The races table depend on the drivers and circuits table, make sure they exist when generating only the races table

Run this to see how to use populate_bd_random.py

    python populate_db_random.py --help





