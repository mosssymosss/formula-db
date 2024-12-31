from faker import Faker
import os
from dotenv import load_dotenv
import random
import requests
import argparse
import sys

load_dotenv()

faker = Faker()

API_BASE_URL = os.getenv("API_BASE_URL")

def generate_drivers(num):
    print(f"Generating {num} drivers...")
    unique_names = [faker.name() for _ in range(int(num/5)*3)]
    for i in range(1, num+1):
        driver = {
            "driver_id": i,
            "number": faker.random_int(min=1, max=99),
            "name": random.choice([random.choice(unique_names) for _ in range(int(num/5)*3)]),
            "nationality": faker.country(),
            "team": random.choice(["Mercedes", "Red Bull", "Ferrari", "McLaren", "Aston Martin", "Alpine", "VCARB", "Kick Sauber", "Haas", "Williams"]),
            "dob": faker.date_of_birth(minimum_age=18, maximum_age=50).strftime("%Y-%m-%d")
        }

        response = requests.post(f"{API_BASE_URL}/drivers/", json=driver)
        if response.status_code == 200:
            print(f"Driver {i} created successfully")
        else:
            print(f"Error creating driver {i}. Status code: {response.status_code}")


def generate_circuits(num):
    print(f"Generating {num} circuits...")
    for i in range(1, num+1):

        info = {
            "description": faker.text(max_nb_chars=200),  
            "created_by": faker.name(),  
            "created_at": faker.date_time_this_decade().isoformat(),  
            "is_active": faker.boolean(),  
            "events_hosted": random.randint(0, 100),  
            "average_attendance": random.randint(10000, 50000)  
        }

        circuit = {
            "circuit_id": i,
            "name": faker.city(),
            "location": faker.country(),
            "length": round(random.uniform(2, 10), 2),
            "laps": faker.random_int(min=50, max=100),
            "lap_record": f"{faker.random_int(min=1, max=2)}:{faker.random_int(min=0, max=59)}:{faker.random_int(min=0, max=59)}",
            "info": info
        }

        response = requests.post(f"{API_BASE_URL}/circuits/", json=circuit)
        if response.status_code == 200:
            print(f"Circuit {i} created successfully")
        else:
            print(f"Error creating circuit {i}. Status code: {response.status_code}")


def generate_races(num, driver_num, circuit_num):
    print(f"Generating {num} races...")
    used = set()
    
    for q in range(num):
        while True:
            driver_id = random.randint(1, driver_num)
            circuit_id = random.randint(1, circuit_num)
            race_date = faker.date_between(start_date="-20y", end_date="today").strftime("%Y-%m-%d")

            if (driver_id, circuit_id, race_date) not in used:
                used.add((driver_id, circuit_id, race_date))
                break

        race_data = {
            "driver_id": driver_id,
            "circuit_id": circuit_id,
            "race_date": race_date,
            "place": faker.random_int(min=1, max=20),
            "points": faker.random_int(min=0, max=25),
            "is_fastest_lap": faker.boolean(),
            "start_place": faker.random_int(min=1, max=20),
        }

        response = requests.post(f"{API_BASE_URL}/races/", json=race_data)
        if response.status_code == 200:
            print(f"Race {q} with {driver_id} circuit {circuit_id} date {race_date} created successfully")
        else:
            print(f"Error creating race with {driver_id} circuit {circuit_id} date {race_date}. Status code: {response.status_code}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Populate database with random data.")
    parser.add_argument("--drivers", type=int, default=4000, help="Number of drivers to generate")
    parser.add_argument("--circuits", type=int, default=4000, help="Number of circuits to generate")
    parser.add_argument("--races", type=int, default=50000, help="Number of races to generate")
    parser.add_argument(
        "--tables",
        type=str,
        nargs="+",
        choices=["drivers", "circuits", "races"],
        default=["drivers", "circuits", "races"],
        help="Specify which tables to generate. Options: drivers, circuits, races. Default: all tables"
    )

    args = parser.parse_args()

    print("Populating database with random data...")
    
    if "drivers" in args.tables:
        generate_drivers(args.drivers)
    if "circuits" in args.tables:
        generate_circuits(args.circuits)
    if "races" in args.tables:
        generate_races(args.races, args.drivers, args.circuits)
    print("Database populated successfully")



