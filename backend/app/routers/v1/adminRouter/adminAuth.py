import json
from fastapi.requests import Request
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.utils.jwt import JWTUserBearer
from app.schemas.userSchema.userResponseSchema import UserResponseSchema
from app.schemas.adminSchema.adminLoginSchema import AdminLoginSchema
from app.utils.hasher import hash_of_sha256
from sqlalchemy.orm import Session
from app.databases.db import get_db
from app.databases.models.admin import Admin
from app.utils.jwt import createUserToken
from app.databases.redis import jwt_admins

AdminAuth = APIRouter(tags=["Authorization of Admins"])


@AdminAuth.post("/admin/login", response_model=UserResponseSchema, responses={
    200: {"description": "Start session of Admin"},
    400: {"content": {
                "application/json": {
                    "example": {"success:": False, "message": "Admin is not exist"}
                }
    }}})
async def login(adminLogin: AdminLoginSchema, db: Session = Depends(get_db)):
    try:
        hash_of_password = await hash_of_sha256(adminLogin.password)
        q = db.query(Admin).filter(Admin.name == adminLogin.login,
                                  Admin.hash_of_password == hash_of_password).first()
        if q:
            data = {"login": adminLogin.login, "password": hash_of_password}
            admin_token = await createUserToken(data, admin=True)
            return JSONResponse(status_code=200, content={"success": True, "access_token": admin_token})
        else:
            return JSONResponse(status_code=400, content={"success": False, "message": "Admin is not exist"})
    except:
        return JSONResponse(status_code=400, content={"success": False, "message": "Admin is not exist"})


@AdminAuth.get("/admin/logout", dependencies=[Depends(JWTUserBearer(admin=True))], responses={
    200: {"description": "End session of Admin", "content": {
                "application/json": {
                    "example": {"success": True}
                }
            }}
})
async def logout(request: Request):
    authorization = request.headers.get("Authorization")
    access_token = authorization.replace("Bearer ", "")
    # Удаляю токен
    await jwt_admins.delete(access_token)
    return JSONResponse(status_code=200, content={"success": True})
