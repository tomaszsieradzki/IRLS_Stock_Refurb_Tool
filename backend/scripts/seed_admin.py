from app.core.config import get_settings
from app.db.session import SessionLocal
from app.domain.auth.models import UserRole
from app.domain.auth.service import AuthService


def main() -> None:
    settings = get_settings()
    db = SessionLocal()
    try:
        service = AuthService(db)
        service.seed_admin_user(
            email=settings.seed_admin_email,
            password=settings.seed_admin_password,
            role=UserRole(settings.seed_admin_role),
        )
        print("Admin user ensured.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
