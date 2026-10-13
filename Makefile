# =============================================================================
# ASHEN-VECTOR — Developer Makefile
# =============================================================================
.PHONY: help install dev-api dev-web test test-unit lint docker-up docker-down

help:
	@echo "ASHEN-VECTOR Developer Commands:"
	@echo "  make install      - Install Python backend & Next.js frontend dependencies"
	@echo "  make dev-api      - Start FastAPI quantitative backend on port 8000"
	@echo "  make dev-web      - Start Next.js research terminal on port 3000"
	@echo "  make test         - Run full pytest suite"
	@echo "  make test-unit    - Run unit and live market pipeline tests"
	@echo "  make docker-up    - Build and launch full stack via Docker Compose"
	@echo "  make docker-down  - Stop Docker Compose services"

install:
	pip install -e ".[dev,ml]"
	cd frontend && npm install

dev-api:
	PYTHONPATH=src python -m uvicorn ashen_vector.api.main:app --host 127.0.0.1 --port 8000 --reload

dev-web:
	cd frontend && npm run dev

test:
	PYTHONPATH=src python -m pytest tests/ -v

test-unit:
	PYTHONPATH=src python -m pytest tests/unit tests/test_live_market.py -v

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
