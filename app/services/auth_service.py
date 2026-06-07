from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin


class AuthService:
    @staticmethod
    async def register(db: AsyncSession, user_in: UserRegister) -> User:
        result = await db.execute(select(User).where(User.email == user_in.email))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(email=user_in.email, hashed_password=hash_password(user_in.password))
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def login(db: AsyncSession, credentials: UserLogin) -> str:
        result = await db.execute(select(User).where(User.email == credentials.email))
        user = result.scalars().first()
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return create_access_token(subject=user.email)
