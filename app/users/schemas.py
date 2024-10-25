from pydantic import BaseModel, EmailStr


# Класс - схема добавления юзера с валидацией типов передаваемых данных
# Эти сырые данные, которые передает пользователь
class SUser(BaseModel):
    email: EmailStr
    password: str