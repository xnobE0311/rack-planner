SHELL := /bin/bash

.PHONY: help backend-install backend-test frontend-install frontend-build check docker-up docker-down

help:
	@echo "Available targets:"
	@echo "  backend-install  Install backend dev dependencies"
	@echo "  backend-test     Run backend pytest suite"
	@echo "  frontend-install Install frontend dependencies"
	@echo "  frontend-build   Build frontend"
	@echo "  check            Run backend tests and frontend build"
	@echo "  docker-up        Start stack with Docker Compose"
	@echo "  docker-down      Stop stack"

backend-install:
	cd backend && python -m pip install --upgrade pip && pip install -e ".[dev]"

backend-test:
	cd backend && pytest -q

frontend-install:
	cd frontend && npm install

frontend-build:
	cd frontend && npm run build

check: backend-test frontend-build

docker-up:
	docker compose up --build

docker-down:
	docker compose down
