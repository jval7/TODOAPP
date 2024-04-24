import unittest
from services import _get_classroom  

class TestGetClassroom(unittest.TestCase):
    def test_easy_task_morning(self):
        classroom = _get_classroom("Fácil", 10)
        self.assertEqual(classroom, "Aula 101")

    def test_easy_task_afternoon(self):
        classroom = _get_classroom("Fácil", 14)
        self.assertEqual(classroom, "Aula 101")

    def test_hard_task_morning(self):
        classroom = _get_classroom("Difícil", 10)
        self.assertEqual(classroom, "Aula 201")

    def test_hard_task_afternoon(self):
        classroom = _get_classroom("Difícil", 14)
        self.assertEqual(classroom, "Aula 201")

    def test_very_hard_task_morning(self):
        classroom = _get_classroom("Muy Difícil", 10)
        self.assertEqual(classroom, "Aula 301")

    def test_very_hard_task_afternoon(self):
        classroom = _get_classroom("Muy Difícil", 14)
        self.assertEqual(classroom, "Aula 302")

if __name__ == '__main__':
    unittest.main()


import unittest
from services import _get_teacher 

class TestGetTeacher(unittest.TestCase):
    def test_easy_task(self):
        teacher = _get_teacher("Fácil", "Tarea fácil de matemáticas")
        self.assertEqual(teacher, "Profesor A")

    def test_hard_task(self):
        teacher = _get_teacher("Difícil", "Tarea difícil de física")
        self.assertEqual(teacher, "Profesor B")

    def test_qualified_teacher(self):
        teacher = _get_teacher("Muy Difícil", "Tarea muy difícil de programación avanzada")
        self.assertIn(teacher, ["Profesor G", "Profesor H"])

    def test_unqualified_teacher(self):
        teacher = _get_teacher("Muy Difícil", "Tarea muy difícil de historia")
        self.assertEqual(teacher, "Profesor por determinar")

if __name__ == '__main__':
    unittest.main()



import unittest
from services import _get_complexity  # Reemplaza 'your_module' con el nombre real de tu módulo

class TestGetComplexity(unittest.TestCase):
    def test_short_description(self):
        description = "Short description"
        self.assertEqual(_get_complexity(description), "Fácil")

    def test_medium_description(self):
        description = "Medium description that is somewhat long"
        self.assertEqual(_get_complexity(description), "Difícil")

    def test_long_description(self):
        description = "A very long description that makes this task extremely difficult"
        self.assertEqual(_get_complexity(description), "Muy Difícil")

if __name__ == '__main__':
    unittest.main()

