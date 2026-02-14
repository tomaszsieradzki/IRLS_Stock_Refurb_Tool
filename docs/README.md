# Backend Auth/RBAC MVP Notes

## Environment variables
- `DATABASE_URL`: Postgres SQLAlchemy URL.
- `JWT_SECRET_KEY`: JWT signing secret (required).
- `JWT_ALGORITHM`: Default `HS256`.
- `JWT_EXP_MINUTES`: Access token expiration in minutes.
- `SEED_ADMIN_EMAIL`: Seeded admin email.
- `SEED_ADMIN_PASSWORD`: Seeded admin password.
- `SEED_ADMIN_ROLE`: Must be one of `admin`, `ops`, `finance`, `viewer` (for MVP use `admin`).

## Endpoints
- Public:
  - `POST /api/v1/auth/login`
  - `GET /api/v1/system/health`
- Authenticated:
  - `GET /api/v1/auth/me`
  - `GET /api/v1/system/whoami`
- RBAC-protected example:
  - `GET /api/v1/system/admin-only` (admin role required)

## Local run
1. `pip install -r backend/requirements.txt`
2. `cd backend && alembic upgrade head`
3. `PYTHONPATH=. python scripts/seed_admin.py`
4. `PYTHONPATH=. uvicorn app.main:app --reload`

## Login example
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@example.com","password":"admin123"}'
```
