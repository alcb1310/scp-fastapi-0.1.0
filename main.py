from fastapi import FastAPI

from src.routes import home
from src import models
from src.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SCP",
    version="0.1.0",
    description="Budgeting application focused on construction companies"
)

app.include_router(home.app)

