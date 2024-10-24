from fastapi.testclient import TestClient
from app import main

client = TestClient(main.app)

def test_should_create_task_when_calling_create_task_endpoint():
    # configurations
    task = {"title": "Task1", "description": "This is a short task"}
    
    # action
    response = client.post("/create_task", json=task)
    response_obj = main.Response(**response.json())

    # assertion
    assert response.status_code == 201
    assert isinstance(response_obj.task_id, str)