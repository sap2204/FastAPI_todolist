from datetime import datetime, timezone
from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from app.config import settings
from app.users.dao import UserDAO


# Получение jwt-токена из запроса пользователя к эндпоинту, в котором нужна аутентификация
def get_token(request: Request):
    token = request.cookies.get("todolist_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Нет jwt-токена")
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITM
        ) # payload - это вторая часть jwt-токена, в которой содержатся данные:
          # id пользователя и время жизни токена
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не является jwt-Токеном")
    expire: str = payload.get("exp") # получаем из данных токена время жизни токена. 
                                     # exp - это ключ, значение которого равно времени жизни токена
    
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()): # если времени жизни токена нет или время жизни токена истекло
                                                                      # 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Время жизни токена закончилось")
    
    user_id: str = payload.get("subject")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Нет id юзера")
    user = await UserDAO.find_by_id(int(user_id)) # поиск юзера в БД по id юзера, который получили из jwt-токена
                                             # юзера из БД записываю в переменную user. user_id ОБЯЗАТЕЛЬНО нужно явно привести к типу int!!!
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Такого пользователя нет в БД")
    return user # на самом деле возвращается модель пользователя


