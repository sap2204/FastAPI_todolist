from datetime import date, time
from sqlalchemy import ForeignKey, Date, Time
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Tasks(Base):
    """Class for creating table tasks in DB"""

    __tablename__ = "tasks"


    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    task: Mapped[str] = mapped_column(nullable=False)
    task_date: Mapped[date] = mapped_column(Date, nullable=False)
    task_time: Mapped[time] = mapped_column(Time, nullable=False)