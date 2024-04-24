from typing import Dict

import uvicorn
from fastapi import FastAPI

from app import services
from app.adapters import DatabaseAdapter

# Create an instance of the FastAPI class
app = FastAPI()

# Set up the database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
DatabaseAdapter(db_url=SQLALCHEMY_DATABASE_URL)


# Define a route for the /get_task_by_id endpoint
@app.get("/get_task_by_id/{task_id}", status_code=200)
def get_task_by_id(task_id: str) -> Dict:
    return services.get_task_by_id(task_id=task_id, db=DatabaseAdapter())


# Define a route for the /create_task endpoint
@app.post("/create_task", status_code=201)
def create_task(task: Dict) -> str:
    return services.create_task(task=task, db=DatabaseAdapter())


if __name__ == "__main__":  # Only input dev
    uvicorn.run(app, host="0.0.0.0", port=8080)
