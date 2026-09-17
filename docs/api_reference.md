# API Reference Architecture

This document outlines the high-performance API layer powering ASHEN-VECTOR's internal microservices and frontend.

## REST Architecture

The backend relies heavily on FastAPI, leveraging Pydantic for strict schema validation and Starlette for asynchronous request handling.

### Inference Endpoints (`/api/predict`)

This endpoint accepts a batch of tickers, fetches the latest feature snapshots from Redis, and returns the aggregated ensemble consensus.

## WebSocket Streaming

For real-time dashboards, WebSockets (`/ws/stream`) push incremental updates of the order book imbalance and tick volatility directly to the client.

### Authentication (JWT)

All endpoints are secured via stateless JSON Web Tokens (JWT), with strict Role-Based Access Control (RBAC) enforced for trade execution endpoints.

## Rate Limiting

Redis-backed sliding window rate limiting prevents accidental self-DDoS during automated high-frequency strategy executions.

