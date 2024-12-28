import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

def create_database():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        cursor.execute(f"CREATE DATABASE {DB_NAME} OWNER {DB_USER};")
        print(f"Database {DB_NAME} created successfully")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

def create_table():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Drivers (
            driver_id INT PRIMARY KEY,
            number INT,
            name VARCHAR(100),
            nationality VARCHAR(50),
            team VARCHAR(50),
            tier VARCHAR(2),
            dob DATE
        );
        """)

        cursor.execute("""
        CREATE TABLE Circuits (
            circuit_id INT PRIMARY KEY,
            name VARCHAR(100),
            location VARCHAR(100),
            length DECIMAL(10, 2),
            laps INT,
            lap_record VARCHAR(50)
        );
        """)

        cursor.execute("""
        CREATE TABLE Races (
            driver_id INT,
            circuit_id INT,
            race_date DATE,
            place INT,
            points INT,
            is_fastest_lap BOOLEAN,
            start_place INT,
            PRIMARY KEY (driver_id, circuit_id, race_date),
            FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id),
            FOREIGN KEY (circuit_id) REFERENCES Circuits(circuit_id)
        );
        """)

        print("Tables created successfully")

        connection.commit()
        cursor.close()
        connection.close()
                       
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    create_database()
    create_table()
                
                      