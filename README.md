# Prime API Monorepo (Baseline)

This repo is reset to a clean microservices baseline per PROJECT_PLAYBOOK.md.

## Structure

- `services/primes`: minimal FastAPI service with `/health`
- `services/api-gateway`: minimal FastAPI gateway with `/health`
- `libs/commons`: shared utilities (errors/result/logger)
- `docs/ARCHITECTURE.md`: structure and evolution
- `.github/workflows/ci.yml`: CI with lint + tests per service

## Local Development

Python 3.11 recommended.

Primes service:

```
pip install -r services/primes/requirements.txt
uvicorn app.main:app --reload --port 8001 --app-dir services/primes
```

API Gateway:

```
pip install -r services/api-gateway/requirements.txt
uvicorn app.main:app --reload --port 8000 --app-dir services/api-gateway
```

## Tests

Run tests per service:

```
pytest -q services/primes
pytest -q services/api-gateway
```

## CI

GitHub Actions runs lint (flake8) and tests for each service.
## Docker

Build and run both services with Compose:

```
docker compose up --build
```

- Gateway: http://localhost:8000 (e.g., `/primes/check?n=7`, `/metrics`)
- Primes: http://localhost:8001 (e.g., `/primes/check?n=7`, `/metrics`)

Stop:

```
docker compose down
```