import unittest
from datetime import datetime, timedelta
from services import _get_deadline, _get_teacher, _get_classroom, _extract_subject, _get_complexity
from unittest.mock import patch




class TestServices(unittest.TestCase):
#-------------------------------------PRUEBAS DE INTEGRACION--------------------------------



#-------------------------------------PRUEBAS UNITARIAS-------------------------------------

#Function: _get_deadline
    def test_deadline_should_be_8_days_from_now(self):
        deadline = _get_deadline()
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")

        deadline_date = deadline_date.date()

        current_date = datetime.utcnow().date()
        expected_deadline = (current_date + timedelta(days=8))

        self.assertEqual(deadline_date, expected_deadline)

#Function _get_complexity
    def test_complexity_for_description_length_less_than_50(self):
        self.assertEqual(_get_complexity('a' * 49), "Fácil")


    def test_complexity_for_description_length_exactly_50(self):
        self.assertEqual(_get_complexity('a' * 50), "Difícil")

    
    def test_complexity_for_description_length_less_than_100(self):
        self.assertEqual(_get_complexity('a' * 99), "Difícil")


    def test_complexity_for_description_length_exactly_100(self):
        self.assertEqual(_get_complexity('a' * 100), "Muy Difícil")


    def test_complexity_for_description_length_more_than_100(self):
        self.assertEqual(_get_complexity('a' * 101), "Muy Difícil")


#Function _get_teacher_
    def test_get_teacher_for_easy_task(self):
        self.assertEqual(_get_teacher('Fácil', 'Tarea de Matemáticas'), "Profesor A")

    def test_get_teacher_for_difficult_task(self):
        self.assertEqual(_get_teacher('Difícil', 'Tarea de Física'), "Profesor B")

    def test_get_teacher_for_very_difficult_task_with_known_subject(self):
        teacher = _get_teacher('Muy Difícil', 'Tarea de Matemáticas')
        self.assertTrue(teacher in ["Profesor C", "Profesor D"])

    def test_get_teacher_for_very_difficult_task_with_unknown_subject(self):
        self.assertEqual(_get_teacher('Muy Difícil', 'Tarea de Ejemplo'), "Profesor por determinar")

#Function _extract_subject
    def test_extract_subject_for_mathematics(self):
        self.assertEqual(_extract_subject('Tarea de Matemáticas'), "Matemáticas")

    def test_extract_subject_for_physics(self):
        self.assertEqual(_extract_subject('Tarea de Física'), "Física")

    def test_extract_subject_for_advanced_programming(self):
        self.assertEqual(_extract_subject('Tarea de Programación Avanzada'), "Programación Avanzada")

    def test_extract_subject_for_other_subject(self):
        self.assertEqual(_extract_subject('Tarea de Ejemplo'), "General")

#Function _get_classroom
    def test_get_classroom_for_easy_task(self):
            self.assertEqual(_get_classroom('Fácil', 10), "Aula 101")

    def test_get_classroom_for_difficult_task(self):
            self.assertEqual(_get_classroom('Difícil', 10), "Aula 201")

    def test_get_classroom_for_very_difficult_task_before_noon(self):
            self.assertEqual(_get_classroom('Muy Difícil', 10), "Aula 301")

    def test_get_classroom_for_very_difficult_task_after_noon(self):
            self.assertEqual(_get_classroom('Muy Difícil', 13), "Aula 302")



if __name__ == '__main__':
    unittest.main()