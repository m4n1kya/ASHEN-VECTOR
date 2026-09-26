# Backend Testing Framework

This document outlines the rigorous testing methodology ensuring zero regressions in the core ASHEN-VECTOR backend services.

## Pytest Architecture

The backend heavily utilizes `pytest` with a deeply nested hierarchy of fixtures defined in `conftest.py` to provide reproducible test states.

## Unit Testing

Pure mathematical functions (e.g., VaR calculation, EWMA smoothing) are tested in strict isolation without touching the disk or network.

### Mocking External APIs

The `responses` library is used to intercept HTTP calls, simulating vendor API rate limits (HTTP 429) to ensure exponential backoff logic works.

## Integration Testing

The `TestClient` from FastAPI is used to execute full request/response lifecycles, ensuring middleware and Pydantic validation operate correctly.

### Database Fixtures

Integration tests utilize Testcontainers to spin up ephemeral Postgres instances, guaranteeing tests never pollute the development database.

## Property-Based Testing

The `hypothesis` library is used to fuzz the risk engine with thousands of randomized input distributions, uncovering complex edge case crashes.

## Load Testing

A `Locust` swarm is configured to simulate 10,000 concurrent web socket connections to the API gateway, verifying the async event loop does not block.

