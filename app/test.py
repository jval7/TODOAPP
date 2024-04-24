import unittest
from datetime import datetime, timedelta
from services import _get_deadline, _get_teacher, _get_classroom, _extract_subject, _get_complexity
from unittest.mock import patch

class TestServices(unittest.TestCase):
    # Pruebas para la función _get_deadline
    def test_deadline_returns_date_8_days_from_current_date(self):
        deadline = _get_deadline()
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
        deadline_date = deadline_date.date()
        current_date = datetime.utcnow().date()
        expected_deadline = (current_date + timedelta(days=8))
        self.assertEqual(deadline_date, expected_deadline)

    # Pruebas para la función _get_complexity
    def test_complexity_returns_easy_for_description_length_less_than_50(self):
        self.assertEqual(_get_complexity('a' * 49), "Fácil")

    def test_complexity_returns_difficult_for_description_length_exactly_50(self):
        self.assertEqual(_get_complexity('a' * 50), "Difícil")

    def test_complexity_returns_difficult_for_description_length_less_than_100(self):
        self.assertEqual(_get_complexity('a' * 99), "Difícil")

    def test_complexity_returns_very_difficult_for_description_length_exactly_100(self):
        self.assertEqual(_get_complexity('a' * 100), "Muy Difícil")

    def test_complexity_returns_very_difficult_for_description_length_more_than_100(self):
        self.assertEqual(_get_complexity('a' * 101), "Muy Difícil")

    # Pruebas para la función _get_teacher
    def test_get_teacher_returns_professor_A_for_easy_task(self):
        self.assertEqual(_get_teacher('Fácil', 'Tarea de Matemáticas'), "Profesor A")

    def test_get_teacher_returns_professor_B_for_difficult_task(self):
        self.assertEqual(_get_teacher('Difícil', 'Tarea de Física'), "Profesor B")

    def test_get_teacher_returns_professor_C_or_D_for_very_difficult_task_with_known_subject(self):
        teacher = _get_teacher('Muy Difícil', 'Tarea de Matemáticas')
        self.assertTrue(teacher in ["Profesor C", "Profesor D"])

    def test_get_teacher_returns_professor_to_be_determined_for_very_difficult_task_with_unknown_subject(self):
        self.assertEqual(_get_teacher('Muy Difícil', 'Tarea de Ejemplo'), "Profesor por determinar")

    # Pruebas para la función _extract_subject
    def test_extract_subject_returns_mathematics_for_mathematics_task(self):
        self.assertEqual(_extract_subject('Tarea de Matemáticas'), "Matemáticas")

    def test_extract_subject_returns_physics_for_physics_task(self):
        self.assertEqual(_extract_subject('Tarea de Física'), "Física")

    def test_extract_subject_returns_advanced_programming_for_advanced_programming_task(self):
        self.assertEqual(_extract_subject('Tarea de Programación Avanzada'), "Programación Avanzada")

    def test_extract_subject_returns_general_for_task_with_unknown_subject(self):
        self.assertEqual(_extract_subject('Tarea de Ejemplo'), "General")

    # Pruebas para la función _get_classroom
    def test_get_classroom_returns_classroom_101_for_easy_task(self):
        self.assertEqual(_get_classroom('Fácil', 10), "Aula 101")

    def test_get_classroom_returns_classroom_201_for_difficult_task(self):
        self.assertEqual(_get_classroom('Difícil', 10), "Aula 201")

    def test_get_classroom_returns_classroom_301_for_very_difficult_task_before_noon(self):
        self.assertEqual(_get_classroom('Muy Difícil', 10), "Aula 301")

    def test_get_classroom_returns_classroom_302_for_very_difficult_task_after_noon(self):
        self.assertEqual(_get_classroom('Muy Difícil', 13), "Aula 302")

if __name__ == '__main__':
    unittest.main()