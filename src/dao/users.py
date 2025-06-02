from src.core.base_methods import BaseDAO
from src.models.users import Users


class UsersDAO(BaseDAO):
    model = Users
