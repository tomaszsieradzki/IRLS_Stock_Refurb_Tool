from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_current_user, require_roles
from app.domain.auth.models import User, UserRole

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/whoami")
def whoami(current_user: Annotated[User, Depends(get_current_user)]) -> dict[str, str]:
    return {"email": current_user.email, "role": current_user.role.value}


@router.get("/admin-only", dependencies=[Depends(require_roles(UserRole.ADMIN))])
def admin_only() -> dict[str, str]:
    return {"message": "admin access granted"}
