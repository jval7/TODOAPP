from datetime import datetime, timedelta
from unittest.mock import patch
from app.services import _get_deadline, _get_complexity, _get_teacher, _extract_subject, _get_classroom



# Pruebas para _get_deadline()
def test_get_deadline():
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.utcnow.return_value = datetime(2024, 4, 30)  # Mock fecha actual
        assert _get_deadline() == "2024-05-08"


# Pruebas para _get_complexity()
def test_get_complexity_easy():
    description = "This is an easy task."
    assert _get_complexity(description) == "Fácil"


def test_get_complexity_difficult():
    description = "This is a more difficult task with a longer description."
    assert _get_complexity(description) == "Difícil"


def test_get_complexity_very_difficult():
    description = "This is a very difficult task with a lengthy description that exceeds 100 charactersssssssssssssssss"
    assert _get_complexity(description) == "Muy Difícil"


# Pruebas para _get_teacher()
def test_get_teacher_easy():
    description = "This is an easy task."
    assert _get_teacher("Fácil", description) == "Profesor A"


def test_get_teacher_difficult():
    description = "This is a more difficult task with a longer description."
    assert _get_teacher("Difícil", description) == "Profesor B"


def test_get_teacher_qualified_subject():
    description = "This is a very difficult task related to Matemáticas."
    with patch('random.choice') as mock_random_choice:
        mock_random_choice.return_value = "Profesor C"  # Mocking random.choice
        assert _get_teacher("Muy Difícil", description) == "Profesor C"


def test_get_teacher_unqualified_subject():
    description = "This is a very difficult task on an unspecified subject."
    assert _get_teacher("Muy Difícil", description) == "Profesor C"


# Pruebas para _extract_subject()
def test_extract_subject():
    description = "This is a task related to Matemáticas."
    assert _extract_subject(description) == "Matemáticas"


# Pruebas para _get_classroom()
def test_get_classroom_easy():
    assert _get_classroom("Fácil", 10) == "Aula 101"


def test_get_classroom_difficult():
    assert _get_classroom("Difícil", 10) == "Aula 201"


def test_get_classroom_very_difficult_before_noon():
    assert _get_classroom("Muy Difícil", 11) == "Aula 301"


def test_get_classroom_very_difficult_after_noon():
    assert _get_classroom("Muy Difícil", 14) == "Aula 302"

############################################################################


def test_singleton_instance():
    adapter1 = DatabaseAdapter(db_url="sqlite:///:memory:")
    adapter2 = DatabaseAdapter(db_url="sqlite:///:memory:")
    assert adapter1 is adapter2
    assert adapter1._initialized is True
