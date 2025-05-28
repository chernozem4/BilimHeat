from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas.user import UserCreate, UserRead
from core.security import hash_password, verify_password
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_create: UserCreate) -> UserRead:
        user = await self.get_user_by_username(user_create.username)
        if user:
            raise HTTPException(status_code=400, detail="Пользователь уже существует")
        hashed_password = hash_password(user_create.password)
        new_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
            is_active=True,
            role="user"
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return UserRead.from_orm(new_user)

    async def get_user_by_username(self, username: str):
        result = await self.db.execute(User.__table__.select().where(User.username == username))
        user_row = result.first()
        return user_row[0] if user_row else None

    async def authenticate_user(self, username: str, password: str) -> UserRead | None:
        user = await self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return UserRead.from_orm(user)
