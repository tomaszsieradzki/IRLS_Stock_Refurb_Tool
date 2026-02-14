from collections.abc import Callable

from fastapi import HTTPException, status

from app.domain.auth.models import User, UserRole


def require_roles(*roles: UserRole) -> Callable[[User], User]:
    def _enforce(user: User) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user

    return _enforce
