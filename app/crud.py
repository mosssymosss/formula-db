from sqlalchemy.orm import Session
from app.models import Driver, Circuit, Race
from app.schemas import DriverCreate, DriverUpdate, CircuitCreate, CircuitUpdate, RaceCreate, RaceUpdate
from typing import List
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

'''
Driver CRUD
'''

def get_drivers(db: Session) -> List[Driver]:
    return db.query(Driver).all()


def get_driver_by_id(db: Session, driver_id: int):
    driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


def create_driver(db: Session, driver: DriverCreate) -> Driver:
    db_driver = Driver(**driver.model_dump())
    db.add(db_driver)
    try:
        db.commit()
        db.refresh(db_driver)
        return db_driver
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Driver already exists or invalid data")


def update_driver(db: Session, driver: DriverUpdate, driver_id: int) -> Driver:
    db_driver = get_driver_by_id(db, driver_id)
    
    for key, value in driver.model_dump().items():
        setattr(db_driver, key, value)
    db.commit()
    db.refresh(db_driver)
    return db_driver


def delete_driver(db: Session, driver_id: int) -> Driver:
    db_driver = get_driver_by_id(db, driver_id)
    db.delete(db_driver)
    db.commit()
    return {"detail": f"Driver {driver_id} has been deleted"}


def get_drivers_filter(db, nationality: str = None, team: str = None, number: int = None, circuit_id: str = None):
    query = db.query(Driver)

    if nationality:
        query = query.filter(Driver.nationality == nationality)
    if team:
        query = query.filter(Driver.team == team)
    if number:
        query = query.filter(Driver.number == number)
    if circuit_id:
        query = query.join(Race).filter(Race.circuit_id == circuit_id)

    drivers = query.all()
    if not drivers:
        raise HTTPException(status_code=404, detail="No drivers found")
    return drivers

'''
Circuit CRUD
'''

def get_circuits(db: Session) -> List[Circuit]:
    return db.query(Circuit).all()

def get_circuit_by_id(db: Session, circuit_id: int):
    circuit = db.query(Circuit).filter(Circuit.circuit_id == circuit_id).first()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit

def create_circuit(db: Session, circuit: CircuitCreate) -> Circuit:
    db_circuit = Circuit(**circuit.model_dump())
    db.add(db_circuit)
    try:
        db.commit()
        db.refresh(db_circuit)
        return db_circuit
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Circuit already exists or invalid data")

def update_circuit(db: Session, circuit: CircuitUpdate, circuit_id: int) -> Circuit:
    db_circuit = get_circuit_by_id(db, circuit_id)
    
    for key, value in circuit.model_dump().items():
        setattr(db_circuit, key, value)
    db.commit()
    db.refresh(db_circuit)
    return db_circuit

def delete_circuit(db: Session, circuit_id: int) -> Circuit:
    db_circuit = get_circuit_by_id(db, circuit_id)

    db.delete(db_circuit)
    db.commit()
    return {"detail": f"Circuit {circuit_id} has been deleted"}

'''
Race CRUD
'''

def get_races(db: Session) -> List[Race]:
    return db.query(Race).all()

def get_race_by_ids(db: Session, driver_id: int, circuit_id: int, race_date):
    race = db.query(Race).filter(
        Race.driver_id == driver_id,
        Race.circuit_id == circuit_id,
        Race.race_date == race_date
    ).first()
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    return race

def create_race(db: Session, race: RaceCreate) -> Race:
    race = Race(**race.model_dump())
    db.add(race)
    try:
        db.commit()
        db.refresh(race)
        return race
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Race already exists or invalid data")
    

def update_race(db: Session, driver_id: int, circuit_id: int, race_date: str, race: RaceUpdate) -> Race:
    db_race = get_race_by_ids(db, driver_id, circuit_id, race_date)
       
    for key, value in race.model_dump().items:
        setattr(db_race, key, value)
    db.commit()
    db.refresh(db_race)
    return db_race


def delete_race(db: Session, driver_id: int, circuit_id: int, race_date: str) -> Race:
    db_race = get_race_by_ids(db, driver_id, circuit_id, race_date)
    db.delete(db_race)
    db.commit() 
    return {"detail": f"Race on {race_date} for driver {driver_id} at circuit {circuit_id} has been deleted"}
    