from fastapi import FastAPI

from src import models
from src.database import engine
from src.routes.authentication import companies, login

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SCP",
    version="0.1.0",
    description="Budgeting application focused on construction companies"
)

app.include_router(login.router)
app.include_router(companies.router)
