import pytest
from datetime import datetime, timedelta
import random

# Mapeos para simplificar las decisiones
teacher_mapping = {
    "Fácil": "Profesor A",
    "Intermedio": "Profesor B",
    "Difícil": "Profesor C",
}

classroom_mapping = {
    "Fácil": "Aula 101",
    "Intermedio": "Aula 201",
    "Difícil": {
        "menos de 10": "Aula 302",
        "más de 10": "Aula 301",
    },
    "Muy Difícil": {
        "menos de 10": "Aula 302",
        "más de 10": "Aula 301",
    },
}

complexity_keywords = {
    "simple": "Fácil",
    "contenido": "Intermedio",
    "mucho texto": "Muy Difícil",
    "mucho esfuerzo": "Muy Difícil",
    "esfuerzo": "Difícil",
}

# Funciones
def _get_deadline():
    # Devuelve la fecha 8 días en el futuro
    return (datetime.utcnow() + timedelta(days=8)).strftime("%Y-%m-%d")

def _get_complexity(description):
    description = description.lower()

    # Busca la primera coincidencia en las palabras clave
    for keyword, complexity in complexity_keywords.items():
        if keyword in description:
            return complexity

    return "Indeterminado"

def _get_teacher(complexity, description):
    description = description.lower()

    # Si la complejidad tiene un mapeo directo, devolver ese valor
    if complexity in teacher_mapping:
        return teacher_mapping[complexity]

    # Lógica adicional para "Muy Difícil"
    if complexity == "Muy Difícil":
        if "matemáticas" in description:
            return "Profesor C"
        elif "física" in description:
            return random.choice(["Profesor D", "Profesor E", "Profesor F"])
        else:
            return "Profesor por determinar"

    return "Profesor por determinar"

def _get_classroom(complexity, student_count):
    # Devuelve la asignación directa para "Fácil" e "Intermedio"
    if complexity in ["Fácil", "Intermedio"]:
        return classroom_mapping[complexity]
    
    # Para "Difícil" y "Muy Difícil", se requiere lógica adicional
    if complexity in ["Difícil", "Muy Difícil"]:
        if student_count > 10:
            return classroom_mapping[complexity]["más de 10"]
        else:
            return classroom_mapping[complexity]["menos de 10"]

    return "Aula por determinar"

def _extract_subject(description):
    description = description.lower()
    
    if "matemáticas" in description:
        return "Matemáticas"
    elif "física" in description:
        return "Física"
    elif "química" in description:
        return "Química"
    else:
        return "Tema por determinar"

# Pruebas unitarias
def test_should_return_correct_deadline():
    expected_deadline = (datetime.utcnow() + timedelta(days=8)).strftime("%Y-%m-%d")
    assert _get_deadline() == expected_deadline

def test_should_return_correct_complexity():
    simple_description = "Tarea simple"
    intermediate_description = "Tarea con un poco más de contenido."
    complex_description = "Tarea con mucho texto y más esfuerzo."

    assert _get_complexity(simple_description) == "Fácil"
    assert _get_complexity(intermediate_description) == "Intermedio"
    assert _get_complexity(complex_description) == "Muy Difícil"

def test_should_return_correct_teacher():
    assert _get_teacher("Fácil", "") == "Profesor A"
    assert _get_teacher("Intermedio", "") == "Profesor B"

    description = "Esta tarea trata sobre temas de matemáticas avanzadas."
    assert _get_teacher("Muy Difícil", description) == "Profesor C"

    description_2 = "Esta tarea trata sobre física."
    assert _get_teacher("Muy Difícil", description_2) in ["Profesor D", "Profesor E", "Profesor F"]

    description_3 = "Esta tarea trata sobre un tema desconocido."
    assert _get_teacher("Muy Difícil", description_3) == "Profesor por determinar"

def test_should_return_correct_classroom():
    assert _get_classroom("Fácil", 10) == "Aula 101"
    assert _get_classroom("Intermedio", 14) == "Aula 201"
    assert _get_classroom("Muy Difícil", 11) == "Aula 301"

    # Para casos indeterminados
    assert _get_classroom("Indeterminado", 10) == "Aula por determinar"

def test_should_return_correct_subject():
    assert _extract_subject("Tarea de matemáticas.") == "Matemáticas"
    assert _extract_subject("Esta es una tarea de física.") == "Física"
