import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, TaskDB
from app.adapters import DatabaseAdapter
from app.services import get_task_by_id, create_task


# Configuración de la base de datos de prueba
@pytest.fixture
def db_adapter():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    adapter = DatabaseAdapter(db_url=None)
    adapter.db = db  # Configura la instancia de la base de datos en el adaptador
    return adapter


@pytest.fixture
def task_dict():
    return {
        'title': 'Estudio integrado',
        'description': 'Descripción detallada para probar el sistema de tareas.'
    }


# Pruebas de integración
def test_create_and_retrieve_task(db_adapter, task_dict):
    # Crea una tarea y verifica la creación
    task_id = create_task(task=task_dict, db=db_adapter)
    assert task_id is not None

    # Recupera la tarea por ID y verifica los campos relevantes
    task_retrieved = get_task_by_id(task_id=task_id, db=db_adapter)
    assert task_retrieved is not None
    assert task_retrieved['title'] == task_dict['title']
    assert task_retrieved['description'] == task_dict['description']
    assert task_retrieved['completed'] == False
    # Verifica otros campos como deadline, complexity, teacher, y classroom
    assert task_retrieved['deadline'] is not None
    assert task_retrieved['complexity'] is not None
    assert task_retrieved['teacher'] is not None
    assert task_retrieved['classroom'] is not None
