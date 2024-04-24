import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from app import services
from app.services import _get_deadline, _get_complexity, _get_teacher, _extract_subject, _get_classroom


class TestGetDeadline(unittest.TestCase):

    def test_get_deadline(self):
        expected_date = (datetime.utcnow() + timedelta(days=8)).strftime("%Y-%m-%d")

        actual_date = _get_deadline()

        self.assertEqual(actual_date, expected_date)

    def test_get_complexity_based_on_input(self):
        descriptions = [
            ("Tarea fácil", "Fácil"),
            ("Esta es una tarea moderadamente difícil de describir", "Difícil"),
            (
                "Esta es una tarea extremadamente difícil que requiere una descripción muy larga y detallada para entenderla completamente.",
                "Muy Difícil")
        ]
        for description, expected_complexity in descriptions:
            assert _get_complexity(description) == expected_complexity

    def test_get_teacher_facil(self):
        complexity = "Fácil"
        description = "fácil"
        assert _get_teacher(complexity, description) == "Profesor A"

    def test_get_teacher_dificil(self):
        complexity = "Difícil"
        description = "difícil"
        assert _get_teacher(complexity, description) == "Profesor B"

    def test_get_teacher_teacher_muy_dificil(self):
        complexity = "Muy Difícil"
        description = "Programación Avanzada: Desarrollo de un sistema de inteligencia artificial"
        assert _get_teacher(complexity, description) in ["Profesor G", "Profesor H"]

    def test_get_teacher_unknown_subject(self):
        complexity = "Muy Difícil"
        description = "Tarea sobre biología molecular"
        assert _get_teacher(complexity, description) == "Profesor por determinar"

    def test_get_teacher_default(self):
        complexity = "Intermedia"
        description = "Tarea intermedia"
        assert _get_teacher(complexity, description) == "Profesor por determinar"

    def test_extract_subject_mathematics(self):
        description = "Este es un problema de matemáticas"
        assert _extract_subject(description) == "Matemáticas"

    def test_extract_subject_physics(self):
        description = "Este es un problema de física"
        assert _extract_subject(description) == "Física"

    def test_extract_subject_programming(self):
        description = "problema de programación avanzada"
        assert _extract_subject(description) == "Programación Avanzada"

    def test_extract_no_encontrado(self):
        description = "problema de química"
        assert _extract_subject(description) == "Materia no encontrada"

    def test_get_classroom_easy_before_noon(self):
        complexity = "Fácil"
        current_hour = 10
        assert _get_classroom(complexity, current_hour) == "Aula 101"

    def test_get_classroom_easy_after_noon(self):
        complexity = "Fácil"
        current_hour = 14
        assert _get_classroom(complexity, current_hour) == "Aula 101"

    def test_get_classroom_difficult(self):
        complexity = "Difícil"
        current_hour = 11
        assert _get_classroom(complexity, current_hour) == "Aula 201"

    def test_get_classroom_difficult0(self):
        complexity = "Difícil"
        current_hour = 15
        assert _get_classroom(complexity, current_hour) == "Aula 201"

    def test_get_classroom_very_difficult1(self):
        complexity = "Muy Difícil"
        current_hour = 11
        assert _get_classroom(complexity, current_hour) == "Aula 301"

    def test_get_classroom_very_difficult2(self):
        complexity = "Muy Difícil"
        current_hour = 15
        assert _get_classroom(complexity, current_hour) == "Aula 302"


if __name__ == '__main__':
    unittest.main()
