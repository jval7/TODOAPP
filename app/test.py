import unittest
from unittest.mock import MagicMock

from services import (_get_deadline, _get_complexity, _get_teacher, _extract_subject, _get_classroom,
create_task,get_task_by_id)
from app.models import Task
from app.adapters import DatabaseAdapter
from datetime import datetime,timedelta

def test_deadline_returns_date_8_days_from_current_date(self):
        deadline = _get_deadline()
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
        deadline_date = deadline_date.date()
        current_date = datetime.utcnow().date()
        expected_deadline = (current_date + timedelta(days=8))
        self.assertEqual(deadline_date, expected_deadline)
class TestGetComplexity(unittest.TestCase):
    def test_complexity_easy(self):
        description = "Esta es una descripción corta."
        result = _get_complexity(description)
        self.assertEqual(result, "Fácil")

    def test_complexity_difficult(self):
        description = "Esta descripción es un poco más larga y está diseñada para probar el límite de dificultad."
        result = _get_complexity(description)
        self.assertEqual(result, "Difícil")

    def test_complexity_very_difficult(self):
        description = "Esta descripción es bastante larga y está específicamente diseñada para superar el umbral y ser clasificada como muy difícil."
        result = _get_complexity(description)
        self.assertEqual(result, "Muy Difícil")

class TestExtractSubject(unittest.TestCase):
    def test_extract_known_subjects(self):
        self.assertEqual(_extract_subject("Resumen de Matemáticas"), "Matemáticas")
        self.assertEqual(_extract_subject("Conceptos básicos de Física"), "Física")
        self.assertEqual(_extract_subject("Introducción a la Programación Avanzada"), "Programación Avanzada")
        self.assertEqual(_extract_subject("Lecciones de Historia"), "Historia")
        self.assertEqual(_extract_subject("Estudios avanzados en Biología"), "Biología")

    def test_extract_no_subject(self):
        self.assertEqual(_extract_subject("Clase sobre un tema no listado"), "Asignatura no especificada")

    def test_case_sensitivity(self):
        self.assertEqual(_extract_subject("matemáticas aplicadas"), "Asignatura no especificada")
        self.assertEqual(_extract_subject("FÍSICA básica"), "Asignatura no especificada")

class TestGetTeacher(unittest.TestCase):
    def test_get_teacher_easy(self):
        complexity = "Fácil"
        description = "Descripción básica de la tarea."
        result = _get_teacher(complexity, description)
        self.assertEqual(result, "Profesor A")

    def test_get_teacher_difficult(self):
        complexity = "Difícil"
        description = "Descripción de tarea intermedia."
        result = _get_teacher(complexity, description)
        self.assertEqual(result, "Profesor B")

    def test_get_teacher_very_difficult_with_subject(self):
        complexity = "Muy Difícil"
        description = "Descripción avanzada de tarea de Programación Avanzada."
        result = _get_teacher(complexity, description)
        self.assertIn(result, ["Profesor G", "Profesor H"])  # Suponiendo que elige aleatoriamente

    def test_get_teacher_very_difficult_without_subject(self):
        complexity = "Muy Difícil"
        description = "Descripción avanzada de tarea sin asignatura específica."
        result = _get_teacher(complexity, description)
        self.assertEqual(result, "Profesor por determinar")

class TestGetClassroom(unittest.TestCase):
    def test_get_classroom_easy(self):
        result = _get_classroom("Fácil", 10)
        self.assertEqual(result, "Aula 101")

    def test_get_classroom_difficult(self):
        result = _get_classroom("Difícil", 10)
        self.assertEqual(result, "Aula 201")

    def test_get_classroom_very_difficult_morning(self):
        result = _get_classroom("Muy Difícil", 11)
        self.assertEqual(result, "Aula 301")

    def test_get_classroom_very_difficult_afternoon(self):
        result = _get_classroom("Muy Difícil", 12)
        self.assertEqual(result, "Aula 302")

    def test_get_classroom_very_difficult_evening(self):
        result = _get_classroom("Muy Difícil", 18)
        self.assertEqual(result, "Aula 302")


class TestGetTaskById(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=DatabaseAdapter)
        self.task_id = 1
        self.db.get_task_by_id.return_value = MagicMock(id=self.task_id, description="Test Task", _sa_instance_state=None)

    def test_get_task_by_id(self):
        task = get_task_by_id(self.task_id, self.db)
        self.db.get_task_by_id.assert_called_once_with(self.task_id)
        self.assertIsInstance(task, dict)
        self.assertEqual(task['id'], self.task_id)
        self.assertEqual(task['description'], "Test Task")
        self.assertNotIn('_sa_instance_state', task)

class TestCreateTask(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=DatabaseAdapter)
        self.task_data = {'description': "Esta tarea es sobre matemáticas avanzadas.", 'other_data': "data"}
        self.expected_task_id = "12345"
        self.db.create_task.return_value = self.expected_task_id

    def create_task(task_data, db):
        # Asegurarse de que todos los campos requeridos están presentes
        task_data_complete = {
            "title": "Título de la tarea",  # Agregar el título requerido
            "description": task_data.get("description", ""),
            "teacher": _get_teacher("Fácil", task_data.get("description", "")),
            "classroom": _get_classroom("Fácil", 10),
            "other_data": task_data.get("other_data", "")
        }
        # Crear la tarea utilizando el diccionario completo
        task_model = Task(**task_data_complete)
        db.create_task(task_model)
        return task_model.id
