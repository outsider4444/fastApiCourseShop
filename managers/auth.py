from datetime import datetime, timedelta
from typing import Optional

import databases
import jwt as jwt
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from models import user


class AuthManager:
    @staticmethod
    def encode_token(self, user):
        try:
            payload = {
                "sub": user["id"],
                "exp": datetime.utcnow() + timedelta(minutes=120)
            }
            return jwt.encode(payload, config("SECRET_KEY"), alghorithm="HS256")
        except Exception as ex:
            raise ex


class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        result = await super().__call__(request)
        try:
            payload = jwt.decode(result.credential, config("SECRET_KEY"), alghorithm="HS256")
            user_data = await databases.fetch_one(user.select().where(user.c.id == payload["sub"]))
            request.state.user = user_data

            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Токен не существует")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Неверный токен")
