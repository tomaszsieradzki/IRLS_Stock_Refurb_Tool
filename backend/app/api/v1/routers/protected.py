from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.dependencies import get_current_user
from app.domain.auth.models import User

router = APIRouter(prefix="/protected", tags=["protected"])


@router.get("/ping")
def protected_ping(current_user: Annotated[User, Depends(get_current_user)]) -> dict[str, str]:
    return {"message": f"pong:{current_user.role.value}"}
