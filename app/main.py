from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.database import Base, engine, get_db
from typing import List
import app.crud as crud

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.delete("/reset/")
def reset_db(db: Session = Depends(get_db)):
    crud.reset_db(db)
    return {"detail": "Database reset"}


'''
Driver Endpoints
'''

@app.post("/drivers/", response_model=schemas.DriverResponse)
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    return crud.create_driver(db, driver)

@app.get("/drivers/", response_model=List[schemas.DriverResponse])
def get_drivers(db: Session = Depends(get_db)):
    return crud.get_drivers(db)

@app.get("/drivers/{driver_id}", response_model=schemas.DriverResponse)
def get_driver_by_id(driver_id: int, db: Session = Depends(get_db)):
    return crud.get_driver_by_id(db=db, driver_id=driver_id)

@app.put("/drivers/{driver_id}", response_model=schemas.DriverResponse)
def update_driver(driver_id: int, driver: schemas.DriverUpdate, db: Session = Depends(get_db)):
    return crud.update_driver(db, driver, driver_id)

@app.delete("/drivers/{driver_id}", response_model=schemas.DriverResponse)
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    return crud.delete_driver(db, driver_id)

@app.get("/drivers/filters/", response_model=List[schemas.DriverResponse])
def get_drivers_filter(db: Session = Depends(get_db), nationality: str = None, team: str = None, number: int = None, circuit_id: str = None):
    return crud.get_drivers_filter(db, nationality, team, number, circuit_id)

@app.get("/drivers/{driver_id}/race_results", response_model=List[schemas.RaceWithCircuitResponse])
def get_driver_races(driver_id: int, db: Session = Depends(get_db)):
    return crud.get_drivers_races(db, driver_id)


'''
Circuit Endpoints
'''

@app.post("/circuits/", response_model=schemas.CircuitResponse)
def create_circuit(circuit: schemas.CircuitCreate, db: Session = Depends(get_db)):
    return crud.create_circuit(db, circuit)

@app.get("/circuits/", response_model=List[schemas.CircuitResponse])
def get_circuits(db: Session = Depends(get_db)):
    return crud.get_circuits(db)

@app.get("/circuits/{circuit_id}", response_model=schemas.CircuitResponse)
def get_circuit_by_id(circuit_id: int, db: Session = Depends(get_db)):
    return crud.get_circuit_by_id(db, circuit_id)

@app.put("/circuits/{circuit_id}", response_model=schemas.CircuitResponse)
def update_circuit(circuit_id: int, circuit: schemas.CircuitUpdate, db: Session = Depends(get_db)):
    return crud.update_circuit(db, circuit, circuit_id)

@app.delete("/circuits/{circuit_id}", response_model=schemas.CircuitResponse)
def delete_circuit(circuit_id: int, db: Session = Depends(get_db)):
    return crud.delete_circuit(db, circuit_id)




'''
Race Endpoints
'''

@app.post("/races/", response_model=schemas.RaceResponse)
def create_race(race: schemas.RaceCreate, db: Session = Depends(get_db)):
    return crud.create_race(db, race)

@app.get("/races/", response_model=List[schemas.RaceResponse])
def get_races(db: Session = Depends(get_db)):
    return crud.get_races(db)

@app.get("/races/{driver_id}/{circuit_id}/{race_date}", response_model=schemas.RaceResponse)
def read_race(driver_id: int, circuit_id: int, race_date: str, db: Session = Depends(get_db)):
    return crud.get_race_by_ids(db, driver_id, circuit_id, race_date)

@app.put("/races/", response_model=schemas.RaceResponse)
def update_race(driver_id: int, circuit_id: int, race_date: str, race: schemas.RaceUpdate, db: Session = Depends(get_db)):
    return crud.update_race(db, driver_id, circuit_id, race_date)

@app.delete("/races/{driver_id}/{circuit_id}/{race_date}", response_model=schemas.RaceResponse)
def delete_race(driver_id: int, circuit_id: int, race_date: str, db: Session = Depends(get_db)):
    return crud.delete_race(db, driver_id, circuit_id, race_date)

