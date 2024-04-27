import random
from datetime import datetime, timedelta
from unittest import TestCase
from app import services
from app.models import Task
from app.adapters import DatabaseAdapter

class TestTaskFunctions(TestCase):
#Estas son las pruebas unitarias 
    def test_get_deadline(self):
        deadline = services._get_deadline()
        self.assertIsInstance(deadline, str)
        self.assertEqual(len(deadline), 10)

    def test_get_complexity(self):
        self.assertEqual(services._get_complexity("Esta es una tarea fácil"), "Fácil")
        self.assertEqual(services._get_complexity("Esta es una tarea difícil con una descripción más larga"), "Difícil")
        self.assertEqual(services._get_complexity("Esta es una tarea muy difícil con una descripción aún más larga"), "Muy Difícil")
        

    def test_get_teacher(self):
        self.assertEqual(services._get_teacher("Fácil", "Tarea de Matemáticas"), "Profesor A")
        self.assertEqual(services._get_teacher("Difícil", "Tarea de Física"), "Profesor B")
        self.assertIn(services._get_teacher("Muy Difícil", "Tarea de Programación Avanzada"), ["Profesor G", "Profesor H"])

    def test_extract_subject(self):
        self.assertEqual(services._extract_subject("Tarea de Matemáticas"), "Matemáticas")
        self.assertEqual(services._extract_subject("Tarea de Física"), "Física")
        self.assertEqual(services._extract_subject("Tarea de Programación Avanzada"), "Programación Avanzada")

    def test_get_classroom(self):
        self.assertEqual(services._get_classroom("Fácil", 10), "Aula 101")
        self.assertEqual(services._get_classroom("Difícil", 14), "Aula 201")
        self.assertEqual(services._get_classroom("Muy Difícil", 8), "Aula 301")
        self.assertEqual(services._get_classroom("Muy Difícil", 16), "Aula 302")

    #PRUEBAS INTEGRACION

    def test_get_task_by_id(self):
        # Suponiendo que hay una tarea con id 1 en la base de datos
        #crear una instancia aqui de la base de datos.
        db = DatabaseAdapter()
        
        task = services.get_task_by_id(1, db)
        self.assertIsNotNone(task)
        self.assertIsInstance(task, dict)
        self.assertIn("id", task)
        self.assertIn("description", task)
        self.assertIn("deadline", task)
        self.assertIn("complexity", task)
        self.assertIn("teacher", task)
        self.assertIn("classroom", task)

    def test_create_task(self):
        task = {
            "description": "Nueva tarea de prueba",
            "deadline": "2024-03-15",
            "complexity": "Fácil",
            "teacher": "Profesor A",
            "classroom": "Aula 101"
        }
        db = DatabaseAdapter()
        task_id = services.create_task(task, db)
        self.assertIsNotNone(task_id)
        self.assertIsInstance(task_id, str)

        # verificar
        db = DatabaseAdapter()
        created_task = services.get_task_by_id(int(task_id), db)
        self.assertIsNotNone(created_task)
        self.assertEqual(created_task["description"], task["description"])
        self.assertEqual(created_task["deadline"], task["deadline"])
        self.assertEqual(created_task["complexity"], task["complexity"])
        self.assertEqual(created_task["teacher"], task["teacher"])
        self.assertEqual(created_task["classroom"], task["classroom"])

if __name__ == '__main__':
    from app.models import Task
    from app.adapters import DatabaseAdapter

    db = DatabaseAdapter()

    services._get_deadline = lambda: (datetime.utcnow() + timedelta(days=8)).strftime("%Y-%m-%d")
    services._get_complexity = lambda description: "Fácil" if len(description) < 50 else "Difícil" if len(description) < 100 else "Muy Difícil"
    services._get_teacher = lambda complexity, description: "Profesor A" if complexity == "Fácil" else "Profesor B" if complexity == "Difícil" else "Profesor C" if complexity == "Muy Difícil" and "Matemáticas" in description else "Profesor D" if complexity == "Muy Difícil" and "Física" in description else "Profesor E" if complexity == "Muy Difícil" and "Programación Avanzada" in description else "Profesor por determinar"
    services._extract_subject = lambda description: "Matemáticas" if "Matemáticas" in description else "Física" if "Física" in description else "Programación Avanzada" if "Programación Avanzada" in description else "Otro"
    services._get_classroom = lambda complexity, current_hour: f"Aula {100 + (1 if complexity == 'Fácil' else 2 if complexity == 'Difícil' else 3 if complexity == 'Muy Difícil' else 0)}-{current_hour // 2}"
