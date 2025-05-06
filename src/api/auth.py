from aiohttp.abc import HTTPException
from fastapi import APIRouter, HTTPException, Response, Request

from src.shemas.user import UserRequestAdd, UserAdd
from src.db import new_session
from src.repository.userRep import UserRepository
from src.service.AuthService import AuthService
from src.api.dependencies import UserDependecies

router = APIRouter(prefix="/users", tags=["Авторизация и Аунтефикация пользователей"])

@router.post("/register")
async def add_user(data: UserRequestAdd):
    async with new_session() as session:
        hashed_password = AuthService.pwd_context.hash(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password, role="USER")
        await UserRepository(session).add_one(new_user_data)
        await session.commit()
        return {"status":"ok"}
    
@router.post("/register-admin")
async def add_user(data: UserRequestAdd):
    async with new_session() as session:
        hashed_password = AuthService.pwd_context.hash(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password, role="ADMIN")
        await UserRepository(session).add_one(new_user_data)
        await session.commit()
        return {"status":"ok"}

@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response):
    async with new_session() as session:
        user = await UserRepository(session).get_user_with_hashed_pass(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")
        acsess_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("acsess_token", acsess_token)
        return {"status":"ok"}

@router.get("/only_login")
async def get_acsess_token(request: Request):
    cookies = request.cookies
    if "acsess_token" in cookies:
        acsess_token = cookies["acsess_token"]
        return acsess_token
    else: return {"status": "not auth(no acsess_token)"}

@router.get("/me")
async def get_me(user_id: UserDependecies):
    async with new_session() as session:
        result = await UserRepository(session).get_one_or_none(id=user_id)
        return result
@router.get("/Logout")
async def log_out(response: Response):
    response.delete_cookie("acsess_token")
    return {"status":"ok"}







