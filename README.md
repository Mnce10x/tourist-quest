# Tourism Performance & Media Intelligence

Production-ready monorepo for ingesting South African tourism public content, extracting KPI/expenditure/media intelligence, and presenting decision-grade dashboards.

## Architecture

### ASCII diagram

```text
        +-----------------------+
        | tourism.gov.za +      |
        | related public sites  |
        +-----------+-----------+
                    |
          sitemap + landing discovery
                    |
            +-------v--------+      +------------------+
            | Worker crawler |----->| Object storage   |
            | + parser/NLP   |      | raw html/pdf +   |
            +-------+--------+      | derived artifacts|
                    |
          structured records + vectors
                    |
             +------v-------------------+
             | Postgres + pgvector      |
             | provenance + audit trails|
             +------+-------------------+
                    |
          +---------v----------+
          | FastAPI analytics  |
          | auth + export APIs |
          +----+-----------+---+
               |           |
      +--------v--+   +----v----------------+
      | React Web |   | Ops/health dashboards|
      +-----------+   +----------------------+
```

### Mermaid

```mermaid
flowchart LR
  S[Public Sources\n(sitemaps, pages, PDFs)] --> C[Worker: Crawl & Discover]
  C --> O[(S3-compatible Object Storage)]
  C --> P[PDF/Page Extraction\n3 fallback strategies]
  P --> N[NLP & Recommendations]
  P --> D[(Postgres + pgvector)]
  N --> D
  D --> A[FastAPI\nOpenAPI + RBAC + rate limits]
  A --> W[React Dashboard\nExecutive/Performance/Expenditure/Media]
  A --> E[CSV/PDF Exports + Explain panels]
```

## Monorepo structure

- `apps/web` – React + Vite + TypeScript dashboard.
- `apps/api` – FastAPI + SQLAlchemy + Alembic + Pydantic.
- `apps/worker` – crawler, parsers, NLP pipeline, queue workers.
- `packages/shared` – shared canonical schemas and enums.

## Quick start (first run)

```bash
make up
make migrate
make seed
make ingest
```

Web app: `http://localhost:5173`
API docs: `http://localhost:8000/docs`

## Setup

1. Copy env template:
   ```bash
   cp .env.example .env
   ```
2. Build and run containers:
   ```bash
   docker compose up --build
   ```

## Developer commands

- `make up` build/start full stack
- `make migrate` run Alembic migrations
- `make seed` seed demo data
- `make ingest` run worker ingestion + persistence
- `make smoke` API smoke checks
- `scripts/validate_runtime.sh` full containerized runtime validation workaround

## Deployment

- Preferred: Render/Fly/DigitalOcean App Platform with containers.
- Configure env vars from `.env.example`.
- Run migrations: `alembic upgrade head`.
- Start worker alongside API.

## Data model (high-level)

- `sources`, `crawl_runs`, `documents`, `document_chunks`
- `kpi_records`, `expenditure_records`
- `media_records`, `recommendations`
- `audit_events`

All analytics and recommendations include provenance (`source_url`, `object_key`, `file_hash`, supporting snippets).

## Adding new sources

1. Add source in `apps/worker/worker/config/sources.py`.
2. Tune crawler and extraction settings in `apps/worker/worker/pipelines/crawler.py` and `apps/worker/worker/extractors/pdf_parser.py`.
3. Add schema mappings in `packages/shared/schemas.py` if new fields appear.
4. Run `python -m worker.run_first_ingest` (or `--no-persist` for dry-run).


## Key API endpoints

- `GET /api/overview` executive cards
- `GET /api/kpi-trends` KPI trend lines
- `GET /api/outliers` variance spikes
- `GET /api/media-lifecycle` story lifecycle
- `GET /api/explain?metric_type=...&metric_id=...` evidence snippets
- `GET /api/data-quality` ingestion/extraction audit (admin role)
- `GET /api/export/{dataset}` CSV snapshots

Role-based access uses `x-role` header (`viewer` or `admin`).


## Requirement amendments and environment workarounds

To close the gap between scaffolded functionality and full production-grade expectations, this repo now uses explicit workaround paths:

- **Container-first validation**: use `scripts/validate_runtime.sh` or `make` targets so host Python/npm dependency drift does not block verification.
- **Offline/blocked-registry environments**: if host package registries are restricted, run checks entirely in Docker images built from repository manifests.
- **Incremental UX hardening**: dashboard pages include interactive charts and explain panels while deeper design-system polish and advanced graph visualizations remain planned extensions.

These amendments ensure a reliable runnable baseline even when local environment constraints prevent direct host installs.

## CI

GitHub Actions workflow `.github/workflows/ci.yml` builds containers, migrates, seeds, runs sample ingest, and executes API smoke checks on each push/PR.

## Testing

```bash
pytest apps/api/tests apps/worker/tests
```

Includes unit, integration-style, and PDF golden-file regression tests.

## Validation checklist

- Health endpoints return OK.
- Ingestion run creates documents and parsed records.
- Dashboard pages render and filter globally.
- CSV export works per view.
- Recommendation cards include confidence + evidence links.
