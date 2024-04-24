from datetime import datetime, timedelta, timezone
from app.services import _get_deadline, _get_complexity, _get_teacher, _extract_subject, _get_classroom, get_task_by_id
from typing import Dict , Optional
from app.adapters import DatabaseAdapter
from app.models import Task, TaskDB


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def test_get_deadline():

    days_until_due = 8
    
    current_utc_time = datetime.now(timezone.utc)
    
    expected_due_date = (current_utc_time + timedelta(days_until_due)).strftime("%Y-%m-%d")
    
    actual_due_date = _get_deadline()
    
    assert actual_due_date == expected_due_date

# Prueba para una descripción corta
def test_get_complexity_easy():
    description = "Tarea fácil"
    assert _get_complexity(description) == "Fácil"

# Prueba para una descripción moderada
def test_get_complexity_difficult():
    description = "Esta es una tarea moderadamente difícil de describir"
    assert _get_complexity(description) == "Difícil"

# Prueba para una descripción larga
def test_get_complexity_very_difficult():
    description = "Esta es una tarea extremadamente difícil que requiere una descripción muy larga y detallada para entenderla completamente."
    assert _get_complexity(description) == "Muy Difícil"

# Prueba para una descripción de longitud exacta del límite inferior
def test_get_complexity_edge_case():
    description = "A" * 49 
    assert _get_complexity(description) == "Fácil"

    # Prueba para una descripción de longitud exacta del límite superior
    description = "A" * 99 
    assert _get_complexity(description) == "Difícil"

# Prueba para una tarea fácil
def test_get_teacher_easy():
    complexity = "Fácil"
    description = "Tarea fácil"
    assert _get_teacher(complexity, description) == "Profesor A"

# Prueba para una tarea difícil
def test_get_teacher_difficult():
    complexity = "Difícil"
    description = "Tarea difícil"
    assert _get_teacher(complexity, description) == "Profesor B"

# Prueba para una tarea de programación avanzada
def test_get_teacher_qualified_teacher():
    complexity = "Muy Difícil"
    description = "Programación Avanzada: Desarrollo de un sistema de inteligencia artificial"
    assert _get_teacher(complexity, description) in ["Profesor G", "Profesor H"]

# Prueba para una tarea con un tema desconocido
def test_get_teacher_unknown_subject():
    complexity = "Muy Difícil"
    description = "Tarea sobre biología molecular"
    assert _get_teacher(complexity, description) == "Profesor por determinar"

# Prueba para una tarea con una complejidad no manejada
def test_get_teacher_default():
    complexity = "Intermedia"
    description = "Tarea intermedia"
    assert _get_teacher(complexity, description) == "Profesor por determinar"
# Prueba para una descripción que contiene "Matemáticas"
def test_extract_subject_mathematics():
    description = "Este es un problema de matemáticas"
    assert _extract_subject(description) == "Matemáticas"

# Prueba para una descripción que contiene "Física"
def test_extract_subject_physics():
    description = "Este es un problema de física"
    assert _extract_subject(description) == "Física"

# Prueba para una descripción que contiene "Programación Avanzada"
def test_extract_subject_programming():
    description = "Este es un problema de programación avanzada"
    assert _extract_subject(description) == "Programación Avanzada"

# Prueba para una descripción que no contiene ninguno de los temas
def test_extract_subject_not_found():
    description = "Este es un problema de química"
    assert _extract_subject(description) == "Materia no encontrada"


# Prueba para una tarea fácil antes del mediodía
def test_get_classroom_easy_before_noon():
    complexity = "Fácil"
    current_hour = 10  # Hora antes del mediodía
    assert _get_classroom(complexity, current_hour) == "Aula 101"

# Prueba para una tarea fácil después del mediodía
def test_get_classroom_easy_after_noon():
    complexity = "Fácil"
    current_hour = 14  # Hora después del mediodía
    assert _get_classroom(complexity, current_hour) == "Aula 101"

 # Prueba para una tarea difícil antes del mediodía
def test_get_classroom_difficult_before_noon():
    complexity = "Difícil"
    current_hour = 11  # Hora antes del mediodía
    assert _get_classroom(complexity, current_hour) == "Aula 201"

# Prueba para una tarea difícil después del mediodía
def test_get_classroom_difficult_after_noon():
    complexity = "Difícil"
    current_hour = 15  # Hora después del mediodía
    assert _get_classroom(complexity, current_hour) == "Aula 201"

# Prueba para una tarea muy difícil antes del mediodía
def test_get_classroom_very_difficult_before_noon():
    complexity = "Muy Difícil"
    current_hour = 11  # Hora antes del mediodía
    assert _get_classroom(complexity, current_hour) == "Aula 301"

def test_get_classroom_very_difficult_after_noon():
    # Prueba para una tarea muy difícil después del mediodía
    complexity = "Muy Difícil"
    current_hour = 15  # Hora después del mediodía
    assert _get_classroom(complexity, current_hour) == "Aula 302"
