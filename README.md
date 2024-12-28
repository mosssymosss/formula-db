# formula-db

Run this command

    pip install -r requirements.txt

You need to have a .env file that has your postgres configurations, i.e.

    POSTGRES_USER={your_username}
    POSTGRES_PASSWORD={your_password}
    POSTGRES_DB={your_database_name}
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432

    DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

Alembic relies on this last parameters

Run the init.db file




