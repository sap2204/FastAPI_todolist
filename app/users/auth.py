from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from pydantic import EmailStr

from app.users.dao import UserDAO
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Хэширование пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Верификация переданного пароля с захэшированным паролем в БД
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Создание JWT-токена
def create_access_token(data: dict) -> str:
    to_encode = data.copy() # копирование входных данных, т.к. словарь - изменяемая структура данных
    expire = datetime.now(timezone.utc) + timedelta(minutes=30) # задание времени жизни токена (с момента создания + 30 мин.)
    to_encode.update({"exp": expire}) # в скопированный входной словарь добавляется ключ exp со значением времени жизни токена
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITM
    ) # создание jwt-токена, данные, ключ и алгоритм шифрования
    return encoded_jwt


# Функция аутентификация юзера
async def authenticate_user(email: EmailStr, password: str):
    existing_user = await UserDAO.find_one_or_none(email = email) # поиск юзера в БД по введенному пользователю email
    # Если по введенному пользователем email нет юзера в БД или введенный пользователем пароль не совпадает с паролем существующего юзера в БД
    if not existing_user or not verify_password(password, existing_user.hashed_password): # existing_user.hashed_password так как в БД столбец называется hashed_password
        return None
    return existing_user

