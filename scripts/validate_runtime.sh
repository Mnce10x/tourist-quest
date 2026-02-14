#!/usr/bin/env bash
set -euo pipefail

echo '[1/6] start stack'
docker compose up --build -d

echo '[2/6] migrate db'
docker compose exec -T api alembic upgrade head

echo '[3/6] seed data'
docker compose exec -T api python -m app.seed_demo

echo '[4/6] run ingest'
docker compose exec -T worker python -m worker.run_first_ingest --no-persist

echo '[5/6] smoke endpoints'
curl -fsS http://localhost:8000/api/health >/dev/null
curl -fsS -H 'x-role: admin' http://localhost:8000/api/overview >/dev/null
curl -fsS -H 'x-role: admin' http://localhost:8000/api/data-quality >/dev/null

echo '[6/6] done: runtime validation passed'
