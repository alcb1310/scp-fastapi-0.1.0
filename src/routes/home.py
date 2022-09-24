from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

app = APIRouter()

@app.get("/")
def home(db: Session=Depends(get_db)):
    test = db.query(models.Test).all()
    return test