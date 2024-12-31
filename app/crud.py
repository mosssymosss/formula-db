from sqlalchemy.orm import Session
from app.models import Driver, Circuit, Race
from app.schemas import DriverCreate, DriverUpdate, CircuitCreate, CircuitUpdate, RaceCreate, RaceUpdate
from typing import List
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import date
from sqlalchemy import func, text



def reset_db(db: Session):
    try:
        delete_all_races(db)
    except HTTPException as e:
        print(e) 
        pass
    try:
        delete_all_drivers(db)
    except HTTPException as e:
        print(e)
        pass
    try:
        delete_all_circuits(db)
    except HTTPException as e:
        print(e)
        pass

'''
Driver CRUD
'''

def get_drivers(db: Session, limit: int = 10, offset: int = 0) -> List[Driver]:
    return db.query(Driver).limit(limit).offset(offset).all()


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


def get_drivers_filter(db: Session, nationality: str = None, team: str = None, number: int = None, circuit_id: str = None, dob: date = None, limit: int = 10, offset: int = 0) -> List[Driver]:
    query = db.query(Driver)

    if nationality:
        query = query.filter(Driver.nationality == nationality)
    if team:
        query = query.filter(Driver.team == team)
    if number:
        query = query.filter(Driver.number == number)
    if circuit_id:
        query = query.join(Race).filter(Race.circuit_id == circuit_id)
    if dob:
        query = query.filter(Driver.dob == dob)

    drivers = query.limit(limit).offset(offset).all()
    if not drivers:
        raise HTTPException(status_code=404, detail="No drivers found")
    return drivers

def delete_all_drivers(db: Session) -> List[Driver]:
    drivers = db.query(Driver).all()
    if not drivers:
        raise HTTPException(status_code=404, detail="No drivers found")
    db.query(Driver).delete()
    db.commit()
    return drivers

def get_drivers_races(db: Session, driver_id: int, limit: int = 10, offset: int = 0) -> List[dict]:
    races = (db.query(Race, Circuit).join(Circuit, Race.circuit_id == Circuit.circuit_id).filter(Race.driver_id == driver_id).limit(limit).offset(offset).all())
    if not races:
        raise HTTPException(status_code=404, detail="No races fount for driver")
    
    return [
        {
            "driver_id": race.Race.driver_id,
            "circuit_id": race.Race.circuit_id,
            "race_date": race.Race.race_date,
            "place": race.Race.place,
            "points": race.Race.points,
            "is_fastest_lap": race.Race.is_fastest_lap,
            "start_place": race.Race.start_place,
            "circuit_details": {
                "name": race.Circuit.name,
                "location": race.Circuit.location,
                "length": race.Circuit.length,
                "laps": race.Circuit.laps,
                "lap_record": race.Circuit.lap_record,
            },
        }
        for race in races
    ]

def get_drivers_total_points(db: Session, driver_id: int, limit: int = 10, offset: int = 0) -> List[dict]:
    query = (
        db.query(Driver.driver_id, Driver.name, Driver.team, func.sum(Race.points).label("total_points"))
        .join(Race, Driver.driver_id == Race.driver_id)
        .group_by(Driver.driver_id, Driver.name, Driver.team)
    )

    if driver_id:
        query = query.filter(Driver.driver_id == driver_id)

    driver_points = query.order_by(func.sum(Race.points).desc()).limit(limit).offset(offset).all()

    if not driver_points:
        raise HTTPException(status_code=404, detail="No drivers found with points data")

    return [
        {
            "driver_id": dp.driver_id,
            "name": dp.name,
            "team": dp.team,
            "total_points": dp.total_points,
        }
        for dp in driver_points
    ]

def get_drivers_with_multiple_wins(db: Session, limit: int = 10, offset: int = 0) -> List[Driver]:
    query = (
        db.query(Driver.driver_id, Driver.name, func.count(Race.circuit_id.distinct()).label("num_circuits"),)
        .join(Race, Driver.driver_id == Race.driver_id)
        .filter(Race.place == 1)
        .group_by(Driver.driver_id, Driver.name)
        .having(func.count(Race.circuit_id.distinct()) > 1)
        .limit(limit).offset(offset)
        .all())
    
    if not query:
        raise HTTPException(status_code=404, detail="No drivers found with wins at multiple circuits")
    
    return [
        {
            "driver_id": q.driver_id,
            "name": q.name,
            "num_circuits": q.num_circuits,
        }
        for q in query
    ]

def get_num_drivers(db: Session) -> dict:
    num_drivers = db.query(Driver).count()
    return {"num_drivers": num_drivers}

'''
Circuit CRUD
'''

def get_circuits(db: Session, limit: int = 10, offset: int = 0) -> List[Circuit]:
    return db.query(Circuit).limit(limit).offset(offset).all()

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

def delete_all_circuits(db: Session) -> List[Circuit]:
    circuits = db.query(Circuit).all()
    if not circuits:
        raise HTTPException(status_code=404, detail="No circuits found")
    db.query(Circuit).delete()
    db.commit()
    return circuits

def get_circuits_with_filter(db: Session, location: str = None, minlength: float = None, maxlength: float = None, minlaps: int = None, maxlaps: int = None, limit: int = 10, offset: int = 0) -> List[Circuit]:
    query = db.query(Circuit)

    if location:
        query = query.filter(Circuit.location == location)
    if minlength:
        query = query.filter(Circuit.length >= minlength)
    if maxlength:
        query = query.filter(Circuit.length <= maxlength)
    if minlaps:
        query = query.filter(Circuit.laps >= minlaps)
    if maxlaps:
        query = query.filter(Circuit.laps <= maxlaps)

    circuits = query.limit(limit).offset(offset).all()
    if not circuits:
        raise HTTPException(status_code=404, detail="No circuits found")
    return circuits


def get_sorted_circuits(db: Session, sort_by: str, limit: int = 10, offset: int = 0) -> List[Circuit]:
    query = db.query(Circuit)

    if sort_by == "length":
        query = query.order_by(Circuit.length.desc())
    elif sort_by == "laps":
        query = query.order_by(Circuit.laps.desc())
    elif sort_by == "lap_record":
        query = query.order_by(Circuit.lap_record)
    else:
        raise HTTPException(status_code=400, detail="Invalid sort_by parameter. You can only sort by length, laps or lap_record")

    circuits = query.limit(limit).offset(offset).all()
    if not circuits:
        raise HTTPException(status_code=404, detail="No circuits found")
    return circuits

def get_most_popular_circuit(db: Session) -> dict:
    query = (db.query(Circuit.name, Circuit.location, func.count(Race.circuit_id).label("num_races"),)
            .join(Race, Circuit.circuit_id == Race.circuit_id)
            .group_by(Circuit.circuit_id, Circuit.name, Circuit.location)
            .order_by(func.count(Race.circuit_id).desc())
            .first())
    
    if not query:
        raise HTTPException(status_code=404, detail="No circuits found")
    
    return {
            "name": query.name,
            "location": query.location,
            "num_races": query.num_races,
            }

def search_info(db: Session, search: str, limit: int = 10, offset: int = 0) -> List[Circuit]:
    sql = text("""
                SELECT * FROM circuits 
                WHERE info::text ~* :search
                LIMIT :limit OFFSET :offset
        """)
    circuits = db.execute(sql, {"search": search, "limit": limit, "offset": offset}).fetchall()
    if not circuits:
        raise HTTPException(status_code=404, detail="No circuits found")
    return circuits

def get_num_circuits(db: Session) -> dict:
    num_circuits = db.query(Circuit).count()
    print(num_circuits)
    return {"num_circuits": num_circuits}

'''

Race CRUD
'''

def get_races(db: Session, limit: int = 10, offset: int = 0) -> List[Race]:
    return db.query(Race).limit(limit).offset(offset).all()

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

def delete_all_races(db: Session) -> List[Race]:
    races = db.query(Race).all()
    if not races:
        raise HTTPException(status_code=404, detail="No races found")
    db.query(Race).delete()
    db.commit()
    return races
    
def get_races_with_filters(db: Session, driver_id: int = None, circuit_id: int = None, start_date: date = None, end_date: date = None, min_points: int = None, max_points: int = None, fastest_lap: bool = None, limit: int = 10, offset: int = 0) -> List[Race]:
    query = db.query(Race)

    if driver_id:
        query = query.filter(Race.driver_id == driver_id)
    if circuit_id:
        query = query.filter(Race.circuit_id == circuit_id)
    if start_date:
        query = query.filter(Race.race_date >= start_date)
    if end_date:
        query = query.filter(Race.race_date <= end_date)
    if min_points:
        query = query.filter(Race.points >= min_points)
    if max_points:
        query = query.filter(Race.points <= max_points)
    if fastest_lap:
        query = query.filter(Race.is_fastest_lap == fastest_lap)

    races = query.limit(limit).offset(offset).all()
    if not races:
        raise HTTPException(status_code=404, detail="No races found")
    return races

def increment_fastest_lap_points(db: Session) -> dict:
    races = db.query(Race).filter(Race.is_fastest_lap == True).all()

    if not races:
        raise HTTPException(status_code=404, detail="No races found where driver had fastest lap")

    for race in races:
        race.points += 1

    db.commit()
    return {"detail": "Fastest lap points have been incremented"}

def get_num_races(db: Session) -> dict:
    num_races = db.query(Race).count()
    return {"num_races": num_races}