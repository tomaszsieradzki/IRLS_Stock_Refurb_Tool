# IRLS Stock Refurb Tool — Project Rules

## 0) Core Delivery Principle (Mandatory)

1. **Do not delete existing files unless explicitly requested in writing.**
2. **Do not rewrite large parts of the codebase in one change.**
3. **Ship in small, incremental commits with clear scope and rollback safety.**
4. Every change must keep the system runnable and testable at all times.

---

## A) Architecture Rules

### A.1 Layered architecture (required)
- Use a strict 3-layer backend architecture:
  - **API layer** (request/response validation + auth checks)
  - **Service layer** (business rules + orchestration)
  - **Repository/DAO layer** (database IO only)
- No business logic in routers/controllers or SQL migration files.
- Frontend follows feature-oriented modules with shared UI primitives.

### A.2 Bounded modules
- Required domain modules:
  - `inventory`
  - `refurbishment`
  - `costing`
  - `vat_customs`
  - `auth`
  - `audit`
- Cross-module calls must happen via service interfaces, not by importing internal module data models directly.

### A.3 API contract stability
- Public API contracts are versioned under `/api/v1`.
- Breaking changes require:
  - new endpoint version or compatibility adapter,
  - migration note in changelog,
  - explicit acceptance by product owner.

### A.4 Single source of truth per concern
- Cost formulas: backend domain service only.
- Status-transition rules: backend domain service only.
- Permission matrix: backend policy engine only.
- Frontend must consume read-only computed fields from API and must not duplicate canonical rules.

---

## B) Naming Conventions

### B.1 General
- English only for identifiers.
- Use descriptive names; avoid abbreviations except accepted domain terms (`VAT`, `SKU`, `HSCode`).

### B.2 Backend (Python)
- Files/modules: `snake_case.py`
- Variables/functions: `snake_case`
- Classes/Pydantic models: `PascalCase`
- Constants/env keys: `UPPER_SNAKE_CASE`
- Database tables/columns: `snake_case`

### B.3 Frontend (React/Vite)
- Component files: `PascalCase.tsx`
- Hooks: `useSomething.ts`
- Utility files: `camelCase.ts` or `snake_case.ts` (pick one and apply consistently per folder)
- Route paths: kebab-case (`/refurb-order/:id`)

### B.4 Naming quality rules
- Booleans must read as predicates (`is_active`, `has_risk_flag`).
- Datetimes must be suffixed `_at` (e.g., `received_at`).
- Monetary values must include currency context (`amount_eur`, `vat_amount_eur`).

---

## C) Backend Structure Rules (FastAPI)

### C.1 Required layout
```text
backend/
  app/
    api/v1/
      routers/
    core/
      config.py
      security.py
      logging.py
    domain/
      <module>/
        models.py
        schemas.py
        service.py
        repository.py
        policy.py
    db/
      base.py
      session.py
    migrations/
    tests/
```

### C.2 Router responsibilities
- Routers must only:
  - parse/validate request,
  - call service methods,
  - map to response schema.
- Routers must not execute SQL and must not implement transition or costing logic.

### C.3 Service responsibilities
- Services must own business workflows, transitions, consistency checks, and domain invariants.
- Services should be deterministic and unit-testable.

### C.4 Repository responsibilities
- Repositories only perform persistence operations.
- No HTTP-layer models in repository signatures.

### C.5 Validation and typing
- All external input validated with Pydantic models.
- Strict typing required for service interfaces and return types.

---

## D) Frontend Structure Rules (React/Vite)

### D.1 Required layout
```text
frontend/
  src/
    app/
      routes/
      providers/
    features/
      inventory/
      refurbishment/
      costing/
      vatCustoms/
      auth/
      audit/
    shared/
      api/
      components/
      hooks/
      utils/
      types/
```

### D.2 Data flow
- Use API client layer in `shared/api` for all server communication.
- No direct `fetch` calls inside random components.
- Forms submit DTOs; server returns computed domain outputs.

### D.3 UI behavior constraints
- Status transition buttons visible only when backend says transition is allowed.
- Monetary summaries shown from backend-calculated fields.
- Risk/deadline alerts (VAT/customs) are read-only reflections of backend state.

### D.4 State management
- Keep state local when possible.
- Use centralized store only for cross-feature session/global state.
- Never duplicate authoritative server data in multiple stores.

---

## E) Database Rules (PostgreSQL Schema + Migrations)

### E.1 Core principles
- PostgreSQL is authoritative system of record.
- Every schema change must be done through migrations (no ad-hoc manual SQL in production).

### E.2 Schema conventions
- Primary keys: `id` as UUID (`uuid_generate_v4()`/equivalent).
- Foreign keys must be explicit with `ON UPDATE`/`ON DELETE` behavior defined.
- Auditable entities include:
  - `created_at`,
  - `updated_at`,
  - `created_by`,
  - `updated_by`.

### E.3 Migration rules
- One migration per atomic change.
- Migrations must include both **upgrade** and **downgrade** paths (unless formally waived).
- Backfill scripts must be idempotent.
- Non-null additions require default/backfill strategy before constraint enforcement.

### E.4 Data integrity constraints
- Use DB constraints for invariants when possible:
  - unique constraints,
  - check constraints (e.g., non-negative costs),
  - FK constraints.
- Complex workflow constraints also validated in service layer.

---

## F) Security Rules (Auth, Roles, Permissions)

### F.1 Authentication
- All non-public endpoints require authenticated user context.
- Tokens/sessions must be time-bound and revocable.

### F.2 Authorization
- Apply RBAC with least privilege.
- Minimum roles:
  - `admin`
  - `ops`
  - `finance`
  - `viewer`
- Authorization checks must be performed server-side for every sensitive action.

### F.3 Permission matrix ownership
- Permission matrix defined in backend policy module.
- Frontend role checks are UX-only and never security controls.

### F.4 Sensitive data handling
- Never log secrets, tokens, or full PII payloads.
- Use environment variables/secrets manager; never hardcode credentials.

---

## G) Logging + Audit Rules (Who changed what, when)

### G.1 Structured logging
- Use structured JSON logs with fields:
  - `timestamp`
  - `level`
  - `service`
  - `trace_id`
  - `user_id` (if available)
  - `entity_type`
  - `entity_id`
  - `action`

### G.2 Audit trail (mandatory for mutable domain entities)
- For each create/update/status transition/delete-equivalent action, record:
  - actor (`user_id`),
  - action type,
  - target entity and id,
  - before/after snapshots (or diff),
  - timestamp (UTC),
  - reason/comment when provided.

### G.3 Immutability and retention
- Audit records are append-only.
- No hard delete of audit rows.
- Retention period must satisfy legal/compliance requirements.

---

## H) Cost Calculation Consistency Rules (Single Source of Truth)

### H.1 Canonical costing engine
- All refurb/cost/profit calculations must be implemented in backend `costing` domain service.
- Frontend may display and format values only.

### H.2 Formula governance
- Cost formula versions must be explicit (`formula_version`).
- Any formula change requires:
  - unit tests for old and new behavior,
  - migration strategy for historic records,
  - release note entry.

### H.3 Deterministic outputs
- Given same inputs + same formula version => same outputs.
- Currency rounding policy must be centralized and consistent (e.g., bankers/half-up, defined once).

### H.4 Recalculation policy
- Recalculation only through explicit service action.
- Store calculation inputs and outputs for auditability.

---

## I) VAT + Customs Tracking Integrity Rules

### I.1 Scope
- Covers non-EU temporary admission tracking, deadlines, and risk exposure values.

### I.2 Required data points per imported item/batch
- `import_reference`
- `origin_country`
- `customs_regime` (must support temporary admission)
- `admission_date`
- `deadline_date`
- `declared_customs_value`
- `estimated_vat_amount`
- `estimated_duty_amount`
- `risk_amount` (potential payable if non-compliant)
- `status` and `status_updated_at`

### I.3 Integrity constraints
- `deadline_date >= admission_date`
- Monetary amounts must be non-negative.
- `risk_amount` must be system-derived from defined risk formula, not manual free text.
- Regime/status changes must be audited.

### I.4 Deadline controls
- System must compute deadline states: `on_track`, `warning`, `overdue`.
- Warning threshold must be configurable (e.g., N days before deadline).
- Overdue records must trigger visible alerts and audit event.

---

## J) Refurbishment Workflow Constraints

### J.1 Allowed statuses (canonical)
1. `received`
2. `inspection`
3. `awaiting_parts`
4. `in_repair`
5. `qa`
6. `ready_for_sale`
7. `sold`
8. `returned`
9. `scrapped`

### J.2 Allowed transitions only
- `received -> inspection`
- `inspection -> awaiting_parts | in_repair | scrapped`
- `awaiting_parts -> in_repair | scrapped`
- `in_repair -> qa | scrapped`
- `qa -> ready_for_sale | in_repair | scrapped`
- `ready_for_sale -> sold | returned`
- `sold -> returned`
- `returned -> inspection | scrapped`

Any other transition is invalid and must be rejected server-side.

### J.3 Required fields by status
- `received`: `received_at`, `source_location`
- `inspection`: `inspection_started_at`, `inspector_id`, `initial_condition`
- `awaiting_parts`: `missing_parts_list`, `parts_eta`
- `in_repair`: `repair_started_at`, `technician_id`, `work_order_ref`
- `qa`: `qa_started_at`, `qa_owner_id`, `qa_checklist_result`
- `ready_for_sale`: `listing_price`, `grade`, `ready_at`
- `sold`: `sold_at`, `sale_reference`, `sale_price`
- `returned`: `returned_at`, `return_reason`
- `scrapped`: `scrapped_at`, `scrap_reason`, `scrap_approval_user_id`

### J.4 Transition enforcement
- Transition must be atomic in one transaction:
  1) validate role/permission,
  2) validate required fields,
  3) persist new status,
  4) emit audit event.

---

## MVP Scope (v0.1.x) vs Later Scope (v1.x)

### v0.1.x (MVP)
- Core authentication + RBAC roles.
- Inventory intake and refurbishment status tracking.
- Canonical costing engine with fixed formula version.
- VAT/customs temporary admission tracking with deadlines and risk amount.
- Basic dashboards and audit trail visibility.
- Migration-managed PostgreSQL schema.

### v1.x (Later scope)
- Advanced forecasting and margin simulations.
- Multi-warehouse optimization and transfer workflows.
- External customs/ERP integrations.
- Configurable formula sets and scenario engine.
- Advanced compliance reporting and automated filing support.

---

## Acceptance Criteria

1. Every domain mutation is authenticated, authorized, validated, and audited.
2. Workflow transitions reject invalid paths and missing required fields.
3. Cost values shown in UI equal backend-calculated values for same record.
4. VAT/customs records enforce deadline integrity and risk tracking.
5. Database schema changes are fully migration-driven and reversible (or documented waiver).
6. Logs include traceable actor + entity context without secret leakage.
7. Build pipeline passes tests, lint checks, and migration checks.

---

## Milestone 1 Checklist (Stability Gate)

- [ ] Project scaffolding includes backend and frontend structure required in this document.
- [ ] Auth + RBAC implemented for `admin`, `ops`, `finance`, `viewer`.
- [ ] Refurbishment statuses and transition guards implemented server-side.
- [ ] Required field validation by status implemented and tested.
- [ ] Canonical costing service implemented with deterministic tests.
- [ ] VAT/customs module tracks temporary admission, deadlines, and risk amount.
- [ ] Audit trail captures actor/action/entity/before-after/timestamp for all mutations.
- [ ] Structured logging includes `trace_id` and user/entity context.
- [ ] Initial PostgreSQL schema created via migrations; upgrade/downgrade verified.
- [ ] API and frontend integration tested for key workflows.
- [ ] CI checks green (tests + lint + migration validation).

---

## Change Management Rules

- All rule changes to this file require:
  1. Pull request with rationale,
  2. Impact analysis (architecture, data, security, operations),
  3. Approval from technical owner.
- If implementation conflicts with this document, this document governs unless formally revised.
