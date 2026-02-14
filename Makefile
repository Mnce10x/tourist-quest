SHELL := /bin/bash

.PHONY: up down logs migrate seed ingest test smoke validate

up:
	docker compose up --build -d

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

migrate:
	docker compose exec api alembic upgrade head

seed:
	docker compose exec api python -m app.seed_demo

ingest:
	docker compose exec worker python -m worker.run_first_ingest

test:
	docker compose exec api pytest /app/tests -q && docker compose exec worker pytest /app/tests -q

smoke:
	curl -fsS http://localhost:8000/api/health
	curl -fsS -H 'x-role: admin' http://localhost:8000/api/overview
	curl -fsS -H 'x-role: admin' http://localhost:8000/api/data-quality

validate:
	./scripts/validate_runtime.sh
