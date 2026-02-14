# IRLS Stock Refurb Tool

Backend MVP auth + RBAC scaffolding is under `backend/`.

## Quick start (backend only)

1. Create and activate a Python 3.11+ virtualenv.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Set environment variables (or create `.env` in repo root):
   ```bash
   DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/irls
   JWT_SECRET_KEY=replace-with-a-strong-secret
   JWT_ALGORITHM=HS256
   JWT_EXP_MINUTES=60
   SEED_ADMIN_EMAIL=admin@example.com
   SEED_ADMIN_PASSWORD=admin123
   SEED_ADMIN_ROLE=admin
   ```
4. Run migrations:
   ```bash
   cd backend
   alembic upgrade head
   ```
5. Seed admin user:
   ```bash
   PYTHONPATH=. python scripts/seed_admin.py
   ```
6. Run API:
   ```bash
   PYTHONPATH=. uvicorn app.main:app --reload
   ```

See `docs/README.md` for endpoint and auth details.
