import random
from datetime import datetime, timedelta
from tarea import (
    _get_deadline,
    _get_complexity,
    _get_teacher,
    _get_classroom,
    _extract_subject
)

def test_get_deadline_returns_correct_format():
    # act
    deadline = _get_deadline()
    # assert
    assert datetime.strptime(deadline, "%Y-%m-%d").date() == (datetime.utcnow() + timedelta(days=8)).date()

def test_get_complexity_returns_correct_value():
    # act
    complexity_easy = _get_complexity("Short description")
    complexity_hard = _get_complexity("Long description that exceeds 100 characters. This is a difficult task.")
    complexity_very_hard = _get_complexity("Very long description that exceeds 200 characters. This is a very difficult task.")
    # assert
    assert complexity_easy == "Fácil"
    assert complexity_hard == "Difícil"
    assert complexity_very_hard == "Muy Difícil"

def test_get_teacher_returns_correct_teacher():
    # act
    teacher_easy = _get_teacher("Fácil", "Math task")
    teacher_hard = _get_teacher("Difícil", "Physics task")
    teacher_very_hard = _get_teacher("Muy Difícil", "Advanced programming task")
    # assert
    assert teacher_easy == "Profesor A"
    assert teacher_hard == "Profesor B"
    assert teacher_very_hard in ["Profesor G", "Profesor H"]  # Since it's random, we check if it's one of the qualified teachers for the subject.

def test_get_classroom_returns_correct_classroom():
    # configuration
    current_hour = datetime.now().hour
    # act
    classroom_easy = _get_classroom("Fácil", current_hour)
    classroom_hard = _get_classroom("Difícil", current_hour)
    classroom_very_hard = _get_classroom("Muy Difícil", current_hour)
    # assert
    assert classroom_easy in ["Aula 101", "Aula 102"]
    assert classroom_hard in ["Aula 201", "Aula 202"]
    assert classroom_very_hard in ["Aula 301", "Aula 302"]