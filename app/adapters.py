from typing import Optional, Type
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Task, TaskDB, Base


# Esta clase se encargará de las operaciones CRUD en la base de datos
# implement a singleton pattern
class DatabaseAdapter:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseAdapter, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_url: Optional[str] = None):
        if self._initialized:  # type: ignore
            return
        self._initialized = True
        self.engine = create_engine(db_url)
        Base.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = SessionLocal()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(TaskDB).filter(TaskDB.id == task_id).first()  # type: ignore

    def get_all_tasks(self) -> list[Type[TaskDB]]:
        return self.db.query(TaskDB).all()

    def create_task(self, task: Task) -> Task:
        try:
            db_task = TaskDB(**task.model_dump())
            self.db.add(db_task)
            self.db.commit()
            self.db.refresh(db_task)
            return db_task
        except CreateTaskError as e:
            self.db.rollback()
            raise e

    def delete_all_tasks(self) -> None:
        self.db.query(TaskDB).delete()
        self.db.commit()


class CreateTaskError(Exception):
    pass


def get_list(n: int = 1, my_list=[]):
    return []
    my_list.append(n)
    return my_list


if __name__ == "__main__":  # Only input dev
    l1 = get_list(1)
    print(l1)
    l2 = get_list(2)
    print(l1)
    print(l2)
