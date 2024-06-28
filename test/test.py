from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch

import pytest  # type: ignore
from app import services
from app.adapters import CreateTaskError, DatabaseAdapter


########### SEGUNDO CORTE - PRUEBAS UNITARIAS ######################


def test_should_get_deadline_when_calling_get_deadline():
    # Arrange
    expected = (datetime.now(timezone.utc) + timedelta(days=8)).strftime("%Y-%m-%d")
    # Act
    result = services._get_deadline()
    # Assert
    assert result == expected


def test_should_get_complexity_when_calling_get_complexity_with_length_less_than_50():
    # Arrange
    description = "Esta es una descripción corta"
    expected = "Fácil"
    # Act
    result = services._get_complexity(description)
    # Assert
    assert result == expected


def test_should_get_complexity_when_calling_get_complexity_with_length_less_than_100():
    # Arrange
    description = "Esta es una descripción un poco más larga que la anterior"
    expected = "Difícil"
    # Act
    result = services._get_complexity(description)
    # Assert
    assert result == expected


def test_should_get_complexity_when_calling_get_complexity_with_length_greater_than_100():
    # Arrange
    description = "Esta es una descripción muy muy muy larga que supera los 100 caracteres y por lo tanto es muy difícil"
    expected = "Muy Difícil"
    # Act
    result = services._get_complexity(description)
    # Assert
    assert result == expected


def test_should_get_teacher_when_calling_get_teacher_with_complexity_easy():
    # Arrange
    complexity = "Fácil"
    description = "Esta es una descripción corta"
    expected = "Profesor A"
    # Act
    result = services._get_teacher(complexity, description)
    # Assert
    assert result == expected


def test_should_get_teacher_when_calling_get_teacher_with_complexity_difficult():
    # Arrange
    complexity = "Difícil"
    description = "Esta es una descripción un poco más larga que la anterior"
    expected = "Profesor B"
    # Act
    result = services._get_teacher(complexity, description)
    # Assert
    assert result == expected


def test_should_get_teacher_when_calling_get_teacher_with_complexity_very_difficult():
    # Arrange
    complexity = "Muy Difícil"
    description = "Tarea de matemáticas muy difícil"
    expected = {"Profesor C", "Profesor D"}

    # Act
    result = services._get_teacher(complexity, description)
    # Assert
    assert result in expected


def test_should_get_teacher_when_calling_get_teacher_with_complexity_very_difficult_and_subject_indeterminate():
    # Arrange
    complexity = "Muy Difícil"
    description = "Esta es una descripción muy muy muy larga que supera los 100 caracteres y por lo tanto es muy difícil y no tiene una materia definida"
    expected = "Profesor por determinar"
    # Act
    result = services._get_teacher(complexity, description)
    # Assert
    assert result == expected


def test_should_extract_subject_when_calling_extract_subject_with_mathematics():
    # Arrange
    description = "Esta es una descripción de Matemáticas"
    expected = "Matemáticas"
    # Act
    result = services._extract_subject(description)
    # Assert
    assert result == expected


def test_should_extract_subject_when_calling_extract_subject_with_physics():
    # Arrange
    description = "Esta es una descripción de Física"
    expected = "Física"
    # Act
    result = services._extract_subject(description)
    # Assert
    assert result == expected


def test_should_extract_subject_when_calling_extract_subject_with_advanced_programming():
    # Arrange
    description = "Esta es una descripción de Programación Avanzada"
    expected = "Programación Avanzada"
    # Act
    result = services._extract_subject(description)
    # Assert
    assert result == expected


def test_should_extract_subject_when_calling_extract_subject_with_other_subject():
    # Arrange
    description = "Esta es una descripción de una materia no definida"
    expected = "Otro"
    # Act
    result = services._extract_subject(description)
    # Assert
    assert result == expected


def test_should_get_classroom_when_calling_get_classroom_with_complexity_easy():
    # Arrange
    complexity = "Fácil"
    current_hour = 10
    expected = "Aula 101"
    # Act
    result = services._get_classroom(complexity, current_hour)
    # Assert
    assert result == expected


def test_should_get_classroom_when_calling_get_classroom_with_complexity_difficult():
    # Arrange
    complexity = "Difícil"
    current_hour = 10
    expected = "Aula 201"
    # Act
    result = services._get_classroom(complexity, current_hour)
    # Assert
    assert result == expected


def test_should_get_classroom_when_calling_get_classroom_with_complexity_very_difficult():
    # Arrange
    complexity = "Muy Difícil"
    current_hour = 10
    expected = "Aula 301"
    # Act
    result = services._get_classroom(complexity, current_hour)
    # Assert
    assert result == expected


def test_should_get_classroom_when_calling_get_classroom_with_complexity_very_difficult_and_hour_after_12():
    # Arrange
    complexity = "Muy Difícil"
    current_hour = 14
    expected = "Aula 302"
    # Act
    result = services._get_classroom(complexity, current_hour)
    # Assert
    assert result == expected


########### PUNTOS OPCIONALES - PRUEBAS DE INTEGRACION ############


def test_should_create_task_when_calling_create_task():
    # Arrange
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    DatabaseAdapter(db_url=SQLALCHEMY_DATABASE_URL)
    task = {
        "title": "Tarea de Matemáticas",
        "description": "Esta es una tarea de matemáticas",
    }
    # Act
    result = services.create_task(task, DatabaseAdapter())
    # Assert
    assert isinstance(result, str), "Expected result to be a string"


def test_should_create_task_when_calling_create_task_with_exception():
    # Arrange
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    adapter = DatabaseAdapter(db_url=SQLALCHEMY_DATABASE_URL)
    task = {
        "title": "Tarea de Matemáticas",
        "description": "Esta es una tarea de matemáticas",
    }
    # Act
    with patch.object(adapter.db, "commit", side_effect=CreateTaskError), patch.object(
        adapter.db, "rollback", new_callable=Mock
    ) as mock_rollback:
        with pytest.raises(CreateTaskError):
            services.create_task(task, adapter)
    # Assert
    assert mock_rollback.called, "Expected rollback to be called"


def test_should_get_task_by_id_when_calling_get_task_by_id():
    # Arrange
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    DatabaseAdapter(db_url=SQLALCHEMY_DATABASE_URL)
    task = {
        "title": "Tarea de Matemáticas",
        "description": "Esta es una tarea de matemáticas",
    }
    task_id = services.create_task(task, DatabaseAdapter())
    # Act
    result = services.get_task_by_id(task_id, DatabaseAdapter())
    # Assert
    assert result is not None
    assert result["id"] == task_id
    assert result["title"] == task["title"]
    assert result["description"] == task["description"]
    assert not result["completed"]
    assert result["deadline"] == services._get_deadline()
    assert result["complexity"] == services._get_complexity(task["description"])
    assert result["teacher"] == services._get_teacher(services._get_complexity(task["description"]), task["description"])
    assert result["classroom"] == services._get_classroom(services._get_complexity(task["description"]), datetime.now().hour)


def test_should_get_all_tasks_when_calling_get_all_tasks():
    # Arrange
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    DatabaseAdapter(db_url=SQLALCHEMY_DATABASE_URL)
    task1 = {
        "title": "Tarea de Matemáticas",
        "description": "Esta es una tarea de matemáticas",
    }
    task2 = {
        "title": "Tarea de Física",
        "description": "Esta es una tarea de física",
    }
    services.create_task(task1, DatabaseAdapter())
    services.create_task(task2, DatabaseAdapter())
    # Act
    result = services.get_all_tasks(DatabaseAdapter())
    # Assert
    # assert len(result) == 2
    assert result[3]["title"] == task1["title"]
    assert result[4]["title"] == task2["title"]
