from typing import List

from beanie import PydanticObjectId
from databases.connections import Database
from fastapi import APIRouter, Depends, HTTPException, status
from models.users import User

router = APIRouter(
    tags=["users"]
)

user_database = Database(User)

# 회원가입
# 새로운 레코드 추가
# {
#     "name": "홍길동",
#     "email": "gildong@example.com",
#     "pswd": "gildong123",
#     "manager": "김매니저",
#     "sellist1": "옵션A",
#     "text": "홍길동의 추가 정보"
# }
@router.post("/new")
async def create_user(body: User) -> dict:
    document = await user_database.save(body)
    return {
        "message": "User created successfully"
        ,"datas": document
    }

# 로그인
@router.get("/{id}", response_model=User)
async def retrieve_event(id: PydanticObjectId) -> User:
    user = await user_database.get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID does not exist"
        )
    return user

# 회원탈퇴
@router.delete("/{id}")
async def delete_user(id: PydanticObjectId) -> dict:
    user = await user_database.get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user = await user_database.delete(id)
    
    return {
        "message": "User deleted successfully."
        ,"datas": user
    }

# 회원수정
from fastapi import Request
@router.put("/{id}", response_model=User)
async def update_event_withjson(id: PydanticObjectId, request:Request) -> User:
    event = await user_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    body = await request.json()
    updated_user = await user_database.update_withjson(id, body)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID does not exist"
        )
    return updated_user

# 모든 회원 data 확인
@router.get("/")
async def retrieve_all_users() -> dict:
    users = await user_database.get_all()
    return {"total_count":len(users)
            , 'datas':users}