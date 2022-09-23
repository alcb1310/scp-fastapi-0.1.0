import imp
from fastapi import FastAPI

app = FastAPI(
    title="SCP",
    version="0.1.0",
    description="Budgeting application focused on construction companies"
)

@app.get("/")
def home():
    return {
        "message": "Hello World!"
    }

