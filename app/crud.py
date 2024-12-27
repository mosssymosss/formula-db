from sqlalchemy.orm import Session
from app.models import Driver, Circuit, Race
from app.schemas import DriverCreate, DriverUpdate, CircuitCreate, CircuitUpdate, RaceCreate, RaceUpdate
from typing import List

'''
Driver CRUD
'''

def get_drivers(db: Session) -> List[Driver]:
    return db.query(Driver).all()


def create_driver(db: Session, driver: DriverCreate) -> Driver:
    db_driver = Driver(**driver.model_dump())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


def update_driver(db: Session, driver: DriverUpdate, driver_id: int) -> Driver:
    db_driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    for key, value in driver.model_dump().items():
        setattr(db_driver, key, value)
    db.commit()
    db.refresh(db_driver)
    return db_driver

def delete_driver(db: Session, driver_id: int) -> Driver:
    db_driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    db.delete(db_driver)
    db.commit()
    return db_driver

'''
Circuit CRUD
'''

def get_circuits(db: Session) -> List[Circuit]:
    return db.query(Circuit).all()

def create_circuit(db: Session, circuit: CircuitCreate) -> Circuit:
    db_circuit = Circuit(**circuit.model_dump())
    db.add(db_circuit)
    db.commit()
    db.refresh(db_circuit)
    return db_circuit

def update_circuit(db: Session, circuit: CircuitUpdate, circuit_id: int) -> Circuit:
    db_circuit = db.query(Circuit).filter(Circuit.circuit_id == circuit_id).first()
    for key, value in circuit.model_dump().items():
        setattr(db_circuit, key, value)
    db.commit()
    db.refresh(db_circuit)
    return db_circuit

def delete_circuit(db: Session, circuit_id: int) -> Circuit:
    db_circuit = db.query(Circuit).filter(Circuit.circuit_id == circuit_id).first()
    db.delete(db_circuit)
    db.commit()
    return db_circuit

'''
Race CRUD
'''

def get_races(db: Session) -> List[Race]:
    return db.query(Race).all()

def create_race(db: Session, race: RaceCreate) -> Race:
    race = Race(**race.model_dump())
    db.add(race)
    db.commit()
    db.refresh(race)
    return race

def update_race(db: Session, driver_id: int, circuit_id: int, race_date: str, race: RaceUpdate) -> Race:
    db_race = db.query(Race).filter(Race.driver_id == driver_id, Race.circuit_id == circuit_id, Race.race_date == race_date).first()   
    for key, value in race.model_dump().items:
        setattr(db_race, key, value)
    db.commit()
    db.refresh(db_race)
    return db_race

def delete_race(db: Session, driver_id: int, circuit_id: int, race_date: str) -> Race:
    db_race = db.query(Race).filter(Race.driver_id == driver_id, Race.circuit_id == circuit_id, Race.race_date == race_date).first()  
    
    db.delete(db_race)
    db.commit() 
    return db_race
    