from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.domain.auth.models import User, UserRole
from app.domain.auth.repository import AuthRepository


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repository = AuthRepository(db)

    def authenticate(self, email: str, password: str) -> str:
        user = self.repository.get_user_by_email(email)
        if not user or not verify_password(password, user.password_hash) or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return create_access_token(user.id)

    def get_user_by_id(self, user_id: UUID) -> User:
        user = self.repository.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")
        return user

    def seed_admin_user(self, email: str, password: str, role: UserRole) -> User:
        existing = self.repository.get_user_by_email(email)
        if existing:
            return existing
        user = User(email=email, password_hash=hash_password(password), is_active=True, role=role)
        return self.repository.create_user(user)
