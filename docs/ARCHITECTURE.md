# Architecture

Repo structure follows Clean Architecture with microservices:

- services/
  - api-gateway/: FastAPI entrypoint for external clients
  - primes/: FastAPI service for prime-related use cases
- libs/commons/: shared errors/result/logger
- docs/: documentation
- .github/workflows/: CI pipeline

Each service evolves into:

- domain/ (pure models)
- usecases/ (application logic)
- ports/ (interfaces)
- adapters/ (infra)
- converters/ (mapping/validation)
- handlers/ (HTTP/RPC controllers)
- tests/