from app.dao.base import BaseDAO
from app.users.model import Users


class UserDAO(BaseDAO):
    model = Users