\# IRLS SYSTEM STATE

\## (Current Backend Implementation Status)



Last update: \[DATE]



---



\# 1. IMPLEMENTED MODULES



\## Machines

\- CRUD endpoints

\- Operate on serial\_number

\- category + size fields exist

\- Model auto-mapping planned (not fully implemented)



\## WorkSessions

\- Start/Stop by serial\_number

\- activity field implemented

\- company field implemented

\- status: running / stopped

\- No pause state



Parallel logic:

\- Non-blocking activities supported (test, report)

\- Worker blocking logic implemented

\- Machine NOT blocked



\## Active endpoints:

GET /api/v1/work/active

GET /api/v1/work/machine/{serial}

GET /api/v1/work/machine/{serial}/active

POST /api/v1/work/start-by-serial

POST /api/v1/work/stop-by-serial



---



\# 2. NOT YET IMPLEMENTED



\- AttendanceSession model

\- Authorized hours logic

\- Extra hours approval flow

\- Progress color calculation

\- Notification engine

\- Offer-hour binding to repair

\- Model → size auto-detection from catalog



---



\# 3. KNOWN LIMITATIONS



\- No attendance guard yet

\- No manager approval logic for extra hours

\- No cost rollup engine

\- No automatic color status calculation



---



\# 4. ARCHITECTURE STATUS



Backend:

\- FastAPI

\- SQLAlchemy

\- Alembic migrations

\- Role enum lowercase

\- Uvicorn reload stable



Business rules partially centralized in WorkService.



---



\# 5. NEXT CORE IMPLEMENTATION



1\. AttendanceSession model

2\. Authorized hours per repair

3\. Extra hours approval workflow

4\. Progress engine

