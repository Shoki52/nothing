import json
from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.databases.models.user import User
from app.databases.redis import jwt_users
from app.schemas.userSchema.userRegisterSchema import UserRegisterSchema
from app.schemas.userSchema.userResponseSchema import UserResponseSchema
from app.databases.db import get_db
from app.utils.hasher import hash_of_sha256
from app.utils.jwt import createUserToken, JWTUserBearer
UserAuth = APIRouter(tags=["Authorization of Users"])


# Регистрация пользователя
@UserAuth.post("/user/register", responses={
    200: {"description": "Create User(To create JWT-token use /user/login)",
          "content": {
              "application/json": {
                  "example": {"success:": True, "message": "User is registered"}
              }
          }
        },
    400: {"content": {
                "application/json": {
                    "example": {"success:": False, "message": "User is exist"}
                }
    }}
        })
async def register(userRegister: UserRegisterSchema, db: Session = Depends(get_db)):
    try:
        hash_of_password = await hash_of_sha256(userRegister.password)
        # Cоздание юзера в БД
        user = User(phone_number=userRegister.phone_int, hash_of_password=hash_of_password)
        db.add(user)
        db.commit()
        # Добавить в Redis
        return JSONResponse(status_code=200, content={"success": True, "message": "User is registered"})
    except:
        # Если вылетит Exception при SQL-запросе, что User уже есть
        return JSONResponse(status_code=400, content={"success": False, "message": "User is exist"})


# Авторизация пользователя
@UserAuth.post("/user/login", response_model=UserResponseSchema, responses={
    200: {"description": "Start session of User"},
    400: {"content": {
                "application/json": {
                    "example": {"success:": False, "message": "User is not exist"}
                }
    }}})
async def login(userRegister: UserRegisterSchema, db: Session = Depends(get_db)):
    try:
        hash_of_password = await hash_of_sha256(userRegister.password)
        # Просмотр в PostgreSQL есть ли хоть один такой юзер, на всякий случай
        q = db.query(User).filter(User.phone_number == userRegister.phone_int, User.hash_of_password == hash_of_password).first()
        # Если есть такой юзер
        if q:
            data = {"phone_int": userRegister.phone_int, "password": hash_of_password}
            user_token = await createUserToken(data)
            return JSONResponse(status_code=200, content={"success": True, "access_token": user_token})
        else:
            return JSONResponse(status_code=400, content={"success": False, "message": "User is not exist"})
    except:
        return JSONResponse(status_code=400, content={"success": False, "message": "User is not exist"})


# Выход пользователя
@UserAuth.get("/user/logout", dependencies=[Depends(JWTUserBearer())], responses={
    200: {"description": "End session of User", "content": {
                "application/json": {
                    "example": {"success": True}
                }
            }}})
async def logout(request: Request):
    # Authorization - хедер, где хранится токен
    authorization = request.headers.get("Authorization")
    # Убираю из начала Bearer
    access_token = authorization.replace("Bearer ", "")
    # Удаляю токен
    await jwt_users.delete(access_token)
    return JSONResponse(status_code=200, content={"success": True})




