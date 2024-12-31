from fastapi import FastAPI, HTTPException, Depends, Query, Request
from sqlalchemy.orm import Session
from app import schemas
from app.database import Base, engine, get_db
from typing import List, Optional
import app.crud as crud
from datetime import date
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

'''
UI
'''

@app.get("/", tags=["UI"])
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# @app.get("/drivers-page/", tags=["UI"])
# def drivers_page(request: Request):
#     return templates.TemplateResponse("drivers.html", {"request": request})

# @app.get("/circuits-page/", tags=["UI"])
# def circuits_page(request: Request):
#     return templates.TemplateResponse("circuits.html", {"request": request})

# @app.get("/races-page/", tags=["UI"])
# def races_page(request: Request):
#     return templates.TemplateResponse("races.html", {"request": request})


'''
Utility Endpoints
'''

@app.delete("/reset/", tags=["Utility"])
def reset_db(db: Session = Depends(get_db)):
    # Reset the database
    try:
        crud.reset_db(db)
        return {"detail": "Database reset"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset database: {str(e)}")


'''
Driver Endpoints
'''

@app.post("/drivers/", response_model=schemas.DriverResponse, tags=["Drivers"])
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    # Create a new driver
    try:
        return crud.create_driver(db, driver)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/drivers/", response_model=List[schemas.DriverResponse], tags=["Drivers"])
def get_drivers(
    db: Session = Depends(get_db), 
    page_size: int = Query(10, gt=0, description="Page size (must be > 0)"), 
    page: int = Query(1, gt=0, description="Page number (must be > 0)")
    ):
    # Get all drivers with pagination
    try:
        return crud.get_drivers(db, page_size, (page - 1) * page_size)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/drivers/{driver_id}", response_model=schemas.DriverResponse, tags=["Drivers"])
def get_driver_by_id(driver_id: int, db: Session = Depends(get_db)):
    # Get a driver by ID
    try:
        return crud.get_driver_by_id(db, driver_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.put("/drivers/{driver_id}", response_model=schemas.DriverResponse, tags=["Drivers"])
def update_driver(driver_id: int, driver: schemas.DriverUpdate, db: Session = Depends(get_db)):
    return crud.update_driver(db, driver, driver_id)

@app.delete("/drivers/{driver_id}", response_model=dict, tags=["Drivers"])
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    # Delete a driver by ID
    try:
        return crud.delete_driver(db, driver_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/drivers/filters/", response_model=List[schemas.DriverResponse], tags=["Drivers"])
def get_drivers_filter(
    db: Session = Depends(get_db), 
    nationality: str = None, 
    team: str = None, 
    number: int = None, 
    circuit_id: str = None, 
    dob: date = None, 
    page_size: int = Query(10, gt=0, description="Page size (must be > 0)"), 
    page: int = Query(1, gt=0, description="Page number (must be > 0)")
    ):
    # Get a paginated list of drivers filtered by nationality, team, number, circuit ID, and/or Date Of Birth.
    try:
        return crud.get_drivers_filter(db, nationality, team, number, circuit_id, dob, page_size, (page - 1) * page_size)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# @app.get("/drivers/{driver_id}/race_results", response_model=List[schemas.RaceWithCircuitResponse], tags=["Drivers"])
# def get_driver_races(
#     driver_id: int, 
#     db: Session = Depends(get_db), 
#     page_size: int = Query(10, gt=0, description="Page size (must be > 0)"), 
#     page: int = Query(1, gt=0, description="Page number (must be > 0)")
#     ):
#     # Get all races for a given driver, including details of the circuit
#     try:
#         return crud.get_drivers_races(db, driver_id, page_size, (page - 1) * page_size)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/drivers/total_points/", response_model=List[schemas.DriverTotalPointsResponse], tags=["Drivers"])
def get_drivers_total_points(
    db: Session = Depends(get_db), 
    driver_id: Optional[int] = None, 
    page_size: int = Query(10, gt=0, description="Page size (must be > 0)"), 
    page: int = Query(1, gt=0, description="Page number (must be > 0)")
    ):
    # Get the total points for each driver, optionally filtered by driver ID
    try:
        return crud.get_drivers_total_points(db, driver_id, page_size, (page - 1) * page_size)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/drivers/multiple_wins/", response_model=List[schemas.DriverMultipleWinsResponse], tags=["Drivers"])
def get_drivers_with_multiple_wins(
    db: Session = Depends(get_db), 
    page_size: int = Query(10, gt=0, description="Page size (must be > 0)"), 
    page: int = Query(1, gt=0, description="Page number (must be > 0)")
    ):
    # Get drivers who have won at multiple circuits
    try:
        return crud.get_drivers_with_multiple_wins(db, page_size, (page - 1) * page_size)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/drivers/driver_count/", response_model=dict, tags=["Drivers"])
def get_num_drivers(db: Session = Depends(get_db)):
    # Get the number of drivers
    try:
        return crud.get_num_drivers(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
'''
Circuit Endpoints
'''

@app.post("/circuits/", response_model=schemas.CircuitResponse, tags=["Circuits"])
def create_circuit(circuit: schemas.CircuitCreate, db: Session = Depends(get_db)):
    # Create a new circuit
    try:
        return crud.create_circuit(db, circuit)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/circuits/", response_model=List[schemas.CircuitResponse], tags=["Circuits"])
def get_circuits(
    db: Session = Depends(get_db), 
    page_size: int = Query(10, gt=0, description="Page size (must be > 0)"), 
    page: int = Query(1, gt=0, description="Page number (must be > 0)")
    ):
    # Get all circuits with pagination
    try:
        return crud.get_circuits(db, page_size, (page - 1) * page_size)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/circuits/{circuit_id}", response_model=schemas.CircuitResponse, tags=["Circuits"])
def get_circuit_by_id(circuit_id: int, db: Session = Depends(get_db)):
    # Get a circuit by ID
    try:
        return crud.get_circuit_by_id(db, circuit_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.put("/circuits/{circuit_id}", response_model=schemas.CircuitResponse, tags=["Circuits"])
def update_circuit(circuit_id: int, circuit: schemas.CircuitUpdate, db: Session = Depends(get_db)):
    # Update a circuit by ID
    try:
        return crud.update_circuit(db, circuit, circuit_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.delete("/circuits/{circuit_id}", response_model=dict, tags=["Circuits"])
def delete_circuit(circuit_id: int, db: Session = Depends(get_db)):
    # Delete a circuit by ID
    try:
        return crud.delete_circuit(db, circuit_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/circuits/filters/", response_model=List[schemas.CircuitResponse], tags=["Circuits"])
def get_circuits_with_filter(
    db: Session = Depends(get_db), 
    location: str = None, 
    minlength: float = None, 
    maxlength: float = None, 
    minlaps: int = None, 
    maxlaps: int = None, 
    page_size: int = Query(10, gt=0, description="Page size (must be > 0)"), 
    page: int = Query(1, gt=0, description="Page number (must be > 0)")
    ):
    # Get a paginated list of circuits filtered by location, length, laps, and/or lap record
    try:
        return crud.get_circuits_with_filter(db, location, minlength, maxlength, minlaps, maxlaps, page_size, (page - 1) * page_size)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/circuits/sorted/", response_model=List[schemas.CircuitResponse], tags=["Circuits"])
def get_sorted_circuits(
    db: Session = Depends(get_db), 
    sort_by: str = None, 
    page_size: int = Query(10, gt=0, description="Page size (must be > 0)"), 
    page: int = Query(1, gt=0, description="Page number (must be > 0)")
    ):
    # Get a paginated list of circuits sorted by name, location, length, or laps
    try:
        return crud.get_sorted_circuits(db, sort_by, page_size, (page - 1) * page_size)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/circuits/most_popular/", response_model=schemas.CircuitPopularityResponse, tags=["Circuits"])
def get_most_popular_circuit(db: Session = Depends(get_db)):
    # Get the most popular circuit
    try:
        return crud.get_most_popular_circuit(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/circuits/search/", response_model=List[schemas.CircuitResponse], tags=["Circuits"])
def search_info(
    db: Session = Depends(get_db), 
    search: str = None, 
    page_size: int = Query(10, gt=0, description="Page size (must be > 0)"), 
    page: int = Query(1, gt=0, description="Page number (must be > 0)")
    ):
    # Search for word in info column of ciruits
    try:
        return crud.search_info(db, search, page_size, page)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/circuits/circuit_count/", response_model=dict, tags=["Circuits"])
def get_num_circuits(db: Session = Depends(get_db)):
    # Get the number of circuits
    try:
        return crud.get_num_circuits(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
'''
Race Endpoints
'''

@app.post("/races/", response_model=schemas.RaceResponse, tags=["Races"])
def create_race(race: schemas.RaceCreate, db: Session = Depends(get_db)):
    # Create a new race
    try:
        return crud.create_race(db, race)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/races/", response_model=List[schemas.RaceResponse], tags=["Races"])
def get_races(
    db: Session = Depends(get_db), 
    page_size: int = Query(10, gt=0, description="Page size (must be > 0)"), 
    page: int = Query(1, gt=0, description="Page number (must be > 0)")
    ):
    # Get all races with pagination
    try:
        return crud.get_races(db, page_size, (page - 1) * page_size)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/races/{driver_id}/{circuit_id}/{race_date}", response_model=schemas.RaceResponse, tags=["Races"])
def read_race(driver_id: int, circuit_id: int, race_date: str, db: Session = Depends(get_db)):
    # Get a race by driver ID, circuit ID and race date
    try:
        return crud.get_race_by_ids(db, driver_id, circuit_id, race_date)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.put("/races/", response_model=schemas.RaceResponse, tags=["Races"])
def update_race(driver_id: int, circuit_id: int, race_date: str, race: schemas.RaceUpdate, db: Session = Depends(get_db)):
    # Update a race by driver ID, circuit ID and race date
    try:
        return crud.update_race(db, driver_id, circuit_id, race_date, race)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.delete("/races/{driver_id}/{circuit_id}/{race_date}", response_model=dict, tags=["Races"])
def delete_race(driver_id: int, circuit_id: int, race_date: str, db: Session = Depends(get_db)):
    # Delete a race by driver ID, circuit ID and race date
    try:
        return crud.delete_race(db, driver_id, circuit_id, race_date)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/races/filters/", response_model=List[schemas.RaceResponse], tags=["Races"])
def get_races_with_filters(
    db: Session = Depends(get_db), 
    driver_id: int = None, 
    circuit_id: int = None, 
    start_date: date = None, 
    end_date: date = None, 
    min_points: int = None, 
    max_points: int = None, 
    fastest_lap: bool = None, 
    page_size: int = Query(10, gt=0, description="Page size (must be > 0)"), 
    page: int = Query(1, gt=0, description="Page number (must be > 0)")
    ):
    # Get a paginated list of races filtered by driver ID, circuit ID, date range, points, and/or fastest lap
    try:
        return crud.get_races_with_filters(db, driver_id, circuit_id, start_date, end_date, min_points, max_points, fastest_lap, page_size, (page - 1) * page_size)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.put("/races/increment_fastest_lap_points/", response_model=dict, tags=["Races"])
def increment_fastest_lap_points(db: Session = Depends(get_db)):
    # Increment points for fastest laps
    try:
        return crud.increment_fastest_lap_points(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/races/race_count/", response_model=dict, tags=["Races"])
def get_num_races(db: Session = Depends(get_db)):
    # Get the number of circuits
    try:
        return crud.get_num_races(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    