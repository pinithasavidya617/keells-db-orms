from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_models import UserCreate, UserResponse, UserUpdate
from database_config import get_db
from user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_create : UserCreate, db: AsyncSession = Depends(get_db)):

    user_repo = UserRepository(db)
    existing_user = await  user_repo.get_user_by_email(user_create.email)
    if existing_user:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
    user = await user_repo.create(user_create)
    return user

@router.delete("/{user_id}")
async def delete_user( user_id:int, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user = await user_repo.delete_user(user_id)
    return user

@router.get("/")
async def get_all_users(
        skip :int = 0,
        limit:int = 10,
        db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    users = await user_repo.get_all_users(skip=skip, limit=limit)
    return users

@router.put("/{user_id}")
async def update_user( user_id:int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user = await user_repo.user_update(user_id=user_id, user_update=user_update)
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user