import json
import time
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from app.configs.config import JWTSettings
from app.databases.redis import jwt_users, jwt_admins
jwtSettings = JWTSettings()


# Создать JWT-токен
async def createUserToken(userRegister: dict, admin: bool = False):
    payload = userRegister
    # Сгорают спустя 24ч
    payload.update({"created_time": time.time()})
    user_token = jwt.encode(payload, jwtSettings.JWT_SECRET_KEY, algorithm=jwtSettings.JWT_ALGORITHM)

    # Создать админу
    if admin:
        await jwt_admins.set(user_token, json.dumps(""), ex=86400)
    # Создать пользователю
    else:
        await jwt_users.set(user_token, json.dumps(""), ex=86400)

    return user_token


# Декодировать его
async def decodeToken(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, jwtSettings.JWT_SECRET_KEY, algorithms=[jwtSettings.JWT_ALGORITHM])
        return decoded_token
    except:
        return {}


# Проверка статуса Токена для Bearer
async def verifyUserToken(token: str, admin: bool = False):
    # Если админ, то смотрим БД с токенами Админов
    if admin:
        data = await jwt_admins.get(token)
    # Иначе БД с токенами Пользователей
    else:
        data = await jwt_users.get(token)

    # Если нет такого токена
    if data is None:
        return False
    # Если есть такой токен
    else:
        return True


# Готовый класс, который создает в OpenAPI окошко с авторизацией, а также валидирует вход на router
class JWTUserBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, admin: bool = False):
        super(JWTUserBearer, self).__init__(auto_error=auto_error)
        # Проверка для админа проверка или обычного пользователя
        self.admin = admin

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTUserBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not await verifyUserToken(credentials.credentials, admin=self.admin):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
