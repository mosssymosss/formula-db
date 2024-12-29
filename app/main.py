from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.database import Base, engine, get_db
from typing import List
import app.crud as crud
from datetime import date

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
def get_drivers_filter(db: Session = Depends(get_db), nationality: str = None, team: str = None, number: int = None, circuit_id: str = None, dob: date = None):
    return crud.get_drivers_filter(db, nationality, team, number, circuit_id, dob)

@app.get("/drivers/{driver_id}/race_results", response_model=List[schemas.RaceWithCircuitResponse])
def get_driver_races(driver_id: int, db: Session = Depends(get_db)):
    return crud.get_drivers_races(db, driver_id)

@app.get("/drivers/total_points/", response_model=List[schemas.DriverTotalPointsResponse])
def get_drivers_total_points(db: Session = Depends(get_db), driver_id: int = None):
    return crud.get_drivers_total_points(db, driver_id)

@app.get("/drivers/multiple_wins/", response_model=List[schemas.DriverMultipleWinsResponse])
def get_drivers_with_multiple_wins(db: Session = Depends(get_db)):
    return crud.get_drivers_with_multiple_wins(db)

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

@app.get("/circuits/filters/", response_model=List[schemas.CircuitResponse])
def get_circuits_with_filter(db: Session = Depends(get_db), location: str = None, minlength: float = None, maxlength: float = None, minlaps: int = None, maxlaps: int = None):
    return crud.get_circuits_with_filter(db, location, minlength, maxlength, minlaps, maxlaps)

@app.get("/circuits/sorted/", response_model=List[schemas.CircuitResponse])
def get_sorted_circuits(db: Session = Depends(get_db), sort_by: str = None):
    return crud.get_sorted_circuits(db, sort_by)

@app.get("/circuits/most-popular/", response_model=schemas.CircuitPopularityResponse)
def get_most_popular_circuit(db: Session = Depends(get_db)):
    return crud.get_most_popular_circuits(db)


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

@app.get("/races/filters/", response_model=List[schemas.RaceResponse])
def get_races_with_filters(db: Session = Depends(get_db), driver_id: int = None, circuit_id: int = None, start_date: date = None, end_date: date = None, min_points: int = None, max_points: int = None, fastest_lap: bool = None):
    return crud.get_races_with_filters(db, driver_id, circuit_id, start_date, end_date, min_points, max_points, fastest_lap)

@app.put("/races/increment_fastest_lap_points/", response_model=List[schemas.RaceResponse])
def increment_fastest_lap_points(db: Session = Depends(get_db)):
    return crud.increment_fastest_lap_points(db)

