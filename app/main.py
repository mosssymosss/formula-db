from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import Base, engine, get_db
from app.models import Driver, Circuit, Race


app = FastAPI()