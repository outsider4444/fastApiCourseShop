from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext

from db import database
from managers.auth import AuthManager
from models import user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Класс, отвечающий за функции пользователя
class UserManager:
    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd_context.hash(user_data["password"])
        try:
            id_ = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "Пользователь с такой почтой уже существует")
        user_do = await database.fetch_one(user.select().where(user.c.id == id_))
        return AuthManager.encode_token(user_do)

    @staticmethod
    async def login(user_data):
        user_do = await database.fetch_one(
            user.select().where(user.c.email == user_data["email"]))  # do - database object
        if not user_do:
            raise HTTPException(400, "Неверная почта или пароль")
        elif not pwd_context.verify(user_data["password"], user_do["password"]):
            raise HTTPException(400, "Неверная почта или пароль")
        return AuthManager.encode_token(user_do)
