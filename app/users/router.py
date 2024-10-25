from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.users.auth import authenticate_user, create_access_token, get_password_hash, verify_password
from app.users.dao import UserDAO
from app.users.model import Users
from app.users.schemas import SUser
from app.users.dependencies import get_current_user


router = APIRouter(
    prefix="/user",
    tags=["Пользователи"]
)



#Эндпоинт регистрации нового пользователя
@router.post("/register", status_code=201)
async def add_new_user(user_data:SUser):
    # Проверка есть ли в БД юзер с таким email
    existing_user = await UserDAO.find_one_or_none(email = user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Такой пользователь уже существует")
    # Хэширование пароля, переданного пользователем
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email = user_data.email, hashed_password = hashed_password)



# Эндпоинт залогинивания пользователя
@router.post("/login", status_code=201)
async def login_user(response: Response, user_data: SUser): # так как работаем с ответом пользователю (отправим токен в куки), то в параметрах функции пишем response: Response
    # Проверка есть ли в БД юзер с таким email и правильный ли пароль 
    existing_user = await authenticate_user(user_data.email, user_data.password)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные email или пароль")
    # Если юзер существует, то создаем токен и отправляем его в куки пользователю
    access_token = create_access_token({"subject": str(existing_user.id)})
    response.set_cookie("todolist_access_token", access_token, httponly=True) # отправляем в куки токен с названием "todolist_access_token"


# Эндпоин выхода из учетной записи
@router.post("/logout", status_code=201)
async def logout_user(response: Response):
    response.delete_cookie("todolist_access_token")
    


# Эндпоинт получения текущего юзера
@router.get("/get_current_user", status_code=201)
async def get_user(user: Users = Depends(get_current_user)):
    return {"id":user.id, "email": user.email}
    


# Эндпоинт удаления текущего юзера
@router.delete("/delete_current_user", status_code=201)
async def delete_user(user: Users = Depends(get_current_user)):
    await UserDAO.delete(id = user.id)
    


    


