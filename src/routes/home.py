from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

app = APIRouter(
    prefix="/api/v1.0",
    tags=["Home"]
)

@app.get("/")
def home(db: Session=Depends(get_db)):
    test = db.query(models.Test).all()
    return test
