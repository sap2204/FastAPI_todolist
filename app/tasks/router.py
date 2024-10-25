from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.tasks.dao import TaskDAO
from app.tasks.model import Tasks
from app.tasks.schemas import STask, SUpdateTask
from app.users.dependencies import get_current_user
from app.users.model import Users


router = APIRouter(
    prefix="/task",
    tags=["Задачи"]
)


# Эндпоинт добавления задачи
@router.post("/add_task", status_code=201)
async def add_task(task_data: STask, 
                   user: Users = Depends(get_current_user)): # task_data - это данные задачи, которые вводятся юзером 
                                     # и они должны соответствовать схеме Task
    await TaskDAO.add(
        user_id = user.id,
        task = task_data.task,
        task_date = task_data.task_date,
        task_time = task_data.task_time
        )



# Эндпоинт получения задачи по id задачи
@router.get("/get/{id_task}", status_code=201)
async def get_task_by_id(id_task: int):
    existing_task = await TaskDAO.find_by_id(id_task)
    if not existing_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задачи с таким id нет")
    return existing_task



# Эндпоинт получения всех задач пользователя
@router.get("/get_all_users_tasks")
async def get_all_tasks(user: Users = Depends(get_current_user)) -> list[STask]:
    return await TaskDAO.find_all(user_id = user.id) # user_id - это название колонки в таблице Tasks, 
                                                    # user.id - это получение из всей строки юзера только значение поля id 



# Эндпоинт обновления задачи по id задачи
@router.patch("/update_task/{id_task}")
async def update_task_by_id(id_task:int, 
                            data_to_update: SUpdateTask,
                            user: Users = Depends(get_current_user)
                            ):
    existing_task = await TaskDAO.find_by_id(id_task) # Получение задачи из БД с id, переданным в запросе
    if not existing_task: # проверка, что задача с id из запроса есть в БД
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Задача с id = {id_task} не найдена")
    if existing_task.user_id != user.id: # проверка, что это задача авторизованного юзера
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Вы не авторизованы")
    
    
    update_task = data_to_update.model_dump(exclude_unset=True) # обновление задачи,
                                                                # извлечение данных из экземпляра модели Pydantic SUpdateTask в виде словаря
                                                                # и получение только тех полей, которые были переданы для обновления
    await TaskDAO.update(id_task, update_task)
    return await TaskDAO.find_by_id(id_task)
    
    



# Эндпоинт удаления задачи по id задачи
@router.delete("/delete_task/{id_task}", status_code=201)
async def delete_task_by_id(id_task: int, user: Users = Depends(get_current_user)):
    task = await TaskDAO.find_by_id(id_task) # проверка, что в БД есть задача с id = id, введенным юзером
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="В БД нет задачи с таким id")
    if task.user_id != user.id: # проверка, что юзер удаляет свою задачу, а не чужую
                                # т.е. в таблице tasks поле user_id Равно id юзера, который обращается к эндпоинту
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="У Вас нет задачи с таким id ")
    await TaskDAO.delete(id = id_task)
    return {"Сообщение": "Задача удалена из БД"}
   
    

 
# Эндпоинт удаления всех задач по id юзера
@router.delete("/delete_all_task")
async def delete_all_task_of_user(user: Users = Depends(get_current_user)):
    await TaskDAO.delete(user_id = user.id)
    return {"Сообщение": "Удалены все Ваши задачи"}

