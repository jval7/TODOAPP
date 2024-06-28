import random
from typing import Optional, Dict
from datetime import datetime, timedelta, timezone
from app.models import Task
from app.adapters import DatabaseAdapter


def get_task_by_id(task_id: int, db: DatabaseAdapter) -> Optional[Dict]:
    task = dict(db.get_task_by_id(task_id).__dict__)
    task.pop("_sa_instance_state", None)
    return task


def get_all_tasks(db: DatabaseAdapter) -> list[Dict]:
    tasks = db.get_all_tasks()
    tasks = [dict(task.__dict__) for task in tasks]  # type: ignore
    [task.pop("_sa_instance_state", None) for task in tasks]
    return tasks  # type: ignore


def create_task(task: Dict, db: DatabaseAdapter) -> str:
    deadline = _get_deadline()
    complexity = _get_complexity(task["description"])
    teacher = _get_teacher(complexity=complexity, description=task["description"])
    current_hour = datetime.now().hour
    classroom = _get_classroom(current_hour=current_hour, complexity=complexity)

    task_model = Task(**task, deadline=deadline, complexity=complexity, teacher=teacher, classroom=classroom)

    db.create_task(task_model)
    return task_model.id


def _get_deadline() -> str:
    return (datetime.now(timezone.utc) + timedelta(days=8)).strftime("%Y-%m-%d")


def _get_complexity(description: str) -> str:
    length = len(description)
    if length < 50:
        return "Fácil"
    elif length < 100:
        return "Difícil"
    else:
        return "Muy Difícil"


def _get_teacher(complexity: str, description: str) -> str:
    teachers = {"Fácil": "Profesor A", "Difícil": "Profesor B", "Muy Difícil": "Profesor C"}
    qualified_teachers = {
        "Matemáticas": ["Profesor C", "Profesor D"],
        "Física": ["Profesor E", "Profesor F"],
        "Programación Avanzada": ["Profesor G", "Profesor H"],
    }
    if complexity == "Fácil":
        return teachers[complexity]
    elif complexity == "Difícil":
        return teachers[complexity]
    else:
        subject = _extract_subject(description)
        if subject in qualified_teachers:
            return random.choice(qualified_teachers[subject])
        else:
            return "Profesor por determinar"


def _extract_subject(description: str) -> str:
    # Implementar
    if "matemáticas" in description.lower():
        return "Matemáticas"
    elif "física" in description.lower():
        return "Física"
    elif "programación avanzada" in description.lower():
        return "Programación Avanzada"
    else:
        return "Otro"


def _get_classroom(complexity: str, current_hour: int) -> str:
    classrooms = {"Fácil": ["Aula 101", "Aula 102"], "Difícil": ["Aula 201", "Aula 202"], "Muy Difícil": ["Aula 301", "Aula 302"]}
    if complexity == "Fácil":
        return classrooms[complexity][0]  # Devuelve la primera aula para tareas fáciles (101)
    elif complexity == "Difícil":
        return classrooms[complexity][0]  # Devuelve la primera aula para tareas difíciles (201)
    else:
        # Lógica para tareas Muy Difíciles
        # En este caso, asignaremos un salón diferente basado en la hora actual

        if current_hour < 12:
            return classrooms["Muy Difícil"][0]  # Asignar Aula 301 si es antes del mediodía
        else:
            return classrooms["Muy Difícil"][1]  # Asignar Aula 302 si es después del mediodía
