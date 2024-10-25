from app.dao.base import BaseDAO
from app.tasks.model import Tasks


# Класс для работы с БД с таблицей Tasks (задачи)
class TaskDAO(BaseDAO):
    model = Tasks