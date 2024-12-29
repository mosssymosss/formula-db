from pydantic import BaseModel
from typing import Optional
from datetime import date



'''
Driver Schemas
'''

class DriverBase(BaseModel):
    driver_id: int
    number: int
    name: str 
    nationality: str 
    team: str
    #tier: str
    dob: date


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    number: Optional[int]
    name: Optional[str]
    nationality: Optional[str]
    team: Optional[str]
    dob: Optional[date]


class DriverResponse(DriverBase):
    class Config:
        from_attributes = True


class DriverTotalPointsResponse(BaseModel):
    driver_id: int
    name: str
    total_points: int
    class Config:
        from_attributes = True


class DriverMultipleWinsResponse(BaseModel):
    driver_id: int
    name: str
    num_circuits: int

'''
Circuit Schemas
'''

class CircuitBase(BaseModel):
    circuit_id: int
    name: str
    location: str
    length: float
    laps: int
    lap_record: str
    info: Optional[dict]


class CircuitCreate(CircuitBase):
    pass


class CircuitUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    length: Optional[float]
    laps: Optional[int]
    lap_record: Optional[str]


class CircuitResponse(CircuitBase):
    class Config:
        from_attributes = True


class CircuitDetail(BaseModel):
    name: str
    location: str
    length: float
    laps: int
    lap_record: str


class CircuitPopularityResponse(BaseModel):
    name: str
    location: str
    num_races: int

'''
Race Schemas
'''

class RaceBase(BaseModel):
    driver_id: int
    circuit_id: int
    race_date: date
    place: int
    points: int
    is_fastest_lap: bool
    start_place: int


class RaceCreate(RaceBase):
    pass


class RaceUpdate(BaseModel):
    place: Optional[int]
    points: Optional[int]
    is_fastest_lap: Optional[bool]


class RaceResponse(RaceBase):
    class Config:
        from_attributes = True

class RaceWithCircuitResponse(RaceBase):
    circuit: CircuitDetail
    class Config:
        from_attributes = True