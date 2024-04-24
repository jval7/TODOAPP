from freezegun import freeze_time
from datetime import datetime, timedelta
from unittest.mock import patch
import random
from app.services import _get_deadline, _get_complexity, _get_teacher, _get_classroom


def test_should_return_correct_deadline_when_calling_get_deadline_method():
    # configuration
    expected_deadline = (datetime.utcnow() + timedelta(days=8)).strftime("%Y-%m-%d")

    # act
    with freeze_time(datetime.utcnow()):
        actual_deadline = _get_deadline()

    # assert
    assert actual_deadline == expected_deadline


def test_should_return_correct_complexity_based_on_description_length():
    # configuration
    descriptions = {
        "Fácil": "Tarea corta",  # length is less than or equal to 50
        "Difícil": "Tarea de longitud media" * 4,  # length is between 51 and 100
        "Muy Difícil": "Tarea muy larga" * 20  # length is greater than 100
    }

    # act and assert
    for expected_complexity, description in descriptions.items():
        actual_complexity = _get_complexity(description)
        assert actual_complexity == expected_complexity


def test_should_return_professor_a_when_complexity_is_easy():
    # Configuración
    complexity = "Fácil"
    description = "Matemáticas"

    # Actuar
    result = _get_teacher(complexity, description)

    # Afirmar
    assert result == "Profesor A"


def test_should_return_professor_b_when_complexity_is_difficult():
    # Configuración
    complexity = "Difícil"
    description = "Física"

    # Actuar
    result = _get_teacher(complexity, description)

    # Afirmar
    assert result == "Profesor B"


def test_should_return_random_qualified_teacher_when_complexity_is_very_difficult(mock_choice):
    # Configuración
    complexity = "Muy Difícil"
    description = "Programación Avanzada"
    mock_choice.return_value = "Profesor G"

    # Actuar
    result = _get_teacher(complexity, description)

    # Afirmar
    assert result == "Profesor G"


@patch('random.choice', return_value="Profesor G")
def test_should_return_random_qualified_teacher_when_complexity_is_very_difficult(mock_choice):
    # Configuración
    complexity = "Muy Difícil"
    description = "Programación Avanzada"

    # Actuar
    result = _get_teacher(complexity, description)

    # Afirmar
    assert result == "Profesor G"


def test_should_return_professor_c_when_complexity_is_very_difficult_and_subject_is_not_in_qualified_teachers():
    # Configuración
    complexity = "Muy Difícil"
    description = "Historia"

    # Actuar
    result = _get_teacher(complexity, description)

    # Afirmar
    assert result == "Profesor D"

def test_should_return_classroom_101_when_complexity_is_easy():
    # Configuración
    complexity = "Fácil"
    current_hour = 10

    # Actuar
    result = _get_classroom(complexity, current_hour)

    # Afirmar
    assert result == "Aula 101"

def test_should_return_classroom_201_when_complexity_is_difficult():
    # Configuración
    complexity = "Difícil"
    current_hour = 10

    # Actuar
    result = _get_classroom(complexity, current_hour)

    # Afirmar
    assert result == "Aula 201"

def test_should_return_classroom_301_when_complexity_is_very_difficult_and_current_hour_is_before_noon():
    # Configuración
    complexity = "Muy Difícil"
    current_hour = 10

    # Actuar
    result = _get_classroom(complexity, current_hour)

    # Afirmar
    assert result == "Aula 301"

def test_should_return_classroom_302_when_complexity_is_very_difficult_and_current_hour_is_after_noon():
    # Configuración
    complexity = "Muy Difícil"
    current_hour = 13

    # Actuar
    result = _get_classroom(complexity, current_hour)

    # Afirmar
    assert result == "Aula 302"

