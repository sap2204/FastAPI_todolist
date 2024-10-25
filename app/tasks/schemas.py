from datetime import date, time
from typing import Optional
from pydantic import BaseModel


# Схема задачи (используется при добавлении новой задачи)
class STask(BaseModel):
    #user_id: int # Это поле не нужно, т.к. есть процесс авторизации, т.е. id получаем из jwt-токена 
    task: str
    task_date: date
    task_time: time



# Схема для обновления задачи методом PATCH
class SUpdateTask(BaseModel):
    task: str | None = None
    task_date: date | None = None
    task_time: time | None = None