from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


# Модель таблицы юзеров
class Users(Base):
    """Class for creating table users in DB"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
     
