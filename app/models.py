from sqlalchemy import Integer, String, Column, ForeignKey, Date, DECIMAL, Boolean, PrimaryKeyConstraint
from database import Base

class Driver(Base):
    __tablename__ = "drivers"

    driver_id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    nationality = Column(String(50), nullable=False)
    team = Column(String(50), nullable=False)
    tier = Column(String(2), nullable=False)
    dob = Column(Date, nullable=False)


class Circuit(Base):
    __tablename__ = "circuits"

    circuit_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    location = Column(String(100))
    length = Column(DECIMAL(10,2))
    laps = Column(Integer)
    lap_record = Column(String(50))


class Race(Base):
    __tablename__ = "races"

    driver_id = Column(Integer, ForeignKey("drivers.driver_id"), primary_key=True)
    circuit_id = Column(Integer, ForeignKey("circuits.circuit_id"), primary_key=True)
    race_date = Column(Date, nullable=False)
    place = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    is_fastest_lap = Column(Boolean, nullable=False)
    start_place = Column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("race_date", "driver_id", "circuit_id"),
    )


