from datetime import datetime, timedelta
from app.services import _get_deadline, _get_complexity, _get_teacher, _get_classroom
from unittest.mock import patch
from app.adapters import DatabaseAdapter
from app.models import Task
import pytest


def test_get_deadline():
    #configuration
    expected_deadline = (datetime.utcnow() + timedelta(days=8)).strftime("%Y-%m-%d")
    #assert
    assert _get_deadline() == expected_deadline


def test_get_complexity_easy():
    # configuration
    description = "Descripción corta"
    #assert
    assert _get_complexity(description) == "Fácil"


def test_get_complexity_difficult():
    # configuration
    description = "Esta es una descripción de longitud media que debería clasificarse como difícil."
    # assert
    assert _get_complexity(description) == "Difícil"


def test_get_complexity_very_difficult():
    # configuration
    description = "Esta es una descripción muy larga que excede los cien caracteres y por tanto debería ser clasificada como Muy Difícil para poder manejar la complejidad adecuadamente y asegurar que todo funcione como se espera."
    # assert
    assert _get_complexity(description) == "Muy Difícil"


def test_get_teacher_easy():
    # configuration
    complexity = "Fácil"
    description = "Descripción simple de matemáticas"
    # assert
    assert _get_teacher(complexity, description) == "Profesor A"


def test_get_teacher_difficult():
    # configuration
    complexity = "Difícil"
    description = "Descripción difícil de física"
    # assert
    assert _get_teacher(complexity, description) == "Profesor B"


@patch('services._extract_subject', return_value="Matemáticas")
@patch('random.choice', return_value="Profesor C")
def test_get_teacher_very_difficult(mock_extract_subject, mock_choice):
    # configuration
    complexity = "Muy Difícil"
    description = "Descripción muy difícil sobre matemáticas avanzadas."
    # assert
    assert _get_teacher(complexity, description) == "Profesor C"


def test_get_classroom_easy():
    # configuration
    complexity = "Fácil"
    current_hour = 10  # Horario de la mañana
    assert _get_classroom(complexity, current_hour) == "Aula 101"


def test_get_classroom_very_difficult_morning():
    # configuration
    complexity = "Muy Difícil"
    current_hour = 11  # Antes del mediodía
    # assert
    assert _get_classroom(complexity, current_hour) == "Aula 301"


def test_get_classroom_very_difficult_afternoon():
    # configuration
    complexity = "Muy Difícil"
    current_hour = 13  # Después del mediodía
    # assert
    assert _get_classroom(complexity, current_hour) == "Aula 302"


##########################################################################
def test_singleton_instance():
    adapter1 = DatabaseAdapter(db_url="sqlite:///:memory:")
    adapter2 = DatabaseAdapter(db_url="sqlite:///:memory:")
    assert adapter1 is adapter2
    assert adapter1._initialized is True


def test_database_initialization():
    adapter = DatabaseAdapter(db_url="sqlite:///:memory:")
    initialized_first_time = adapter._initialized
    adapter2 = DatabaseAdapter(db_url="sqlite:///:memory:")
    initialized_second_time = adapter2._initialized
    assert initialized_first_time is True
    assert initialized_second_time is True  # Debe ser True porque es la misma instancia


def test_create_task_success(db_adapter):
    task_dict = {
        "title": "New Task",
        "description": "Task description",
        "completed": False,
        "deadline": "2024-12-31",
        "complexity": "Fácil",
        "teacher": "Profesor A",
        "classroom": "Aula 101"
    }
    task_model = Task(**task_dict)
    created_task = db_adapter.create_task(task_model)
    assert created_task.id is not None
    assert created_task.title == "New Task"


def test_create_task_exception_handling(db_adapter):
    task_dict = {
        "title": "New Task",
        # Provocar un error, por ejemplo, omitir un campo obligatorio o pasar datos erróneos
    }
    with pytest.raises(Exception):
        db_adapter.create_task(Task(**task_dict))