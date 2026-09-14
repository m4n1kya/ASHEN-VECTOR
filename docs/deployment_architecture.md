# Deployment and Infrastructure Architecture

This document outlines the robust infrastructure utilized to host, scale, and secure ASHEN-VECTOR.

## Core Principles

Our infrastructure prioritizes extreme low-latency, zero-downtime deployments, and rigid security protocols for financial data.

## Cloud Strategy

We employ a hybrid cloud architecture, utilizing AWS for heavy ML compute and Vercel's Edge Network for global frontend distribution.

### Containerization

The FastAPI backend, data ingestion workers, and ML inference engines are fully containerized using Docker.

#### Multi-stage Builds

Multi-stage Docker builds ensure that compilers and heavy build tools are stripped from the final lightweight production images.

## Orchestration (Kubernetes)

Containers are orchestrated via Amazon EKS (Elastic Kubernetes Service), abstracting away underlying EC2 node management.

### Auto-Scaling

Horizontal Pod Autoscalers (HPA) scale the inference pods dynamically based on CPU utilization during market open and close spikes.

#### GPU Scheduling

Node affinity rules ensure that heavy deep learning inference pods are exclusively scheduled on accelerated `p4d` instances with NVIDIA A100s.

### Helm Charts

Complex deployments are templated using Helm, allowing for reproducible staging and production environments from a single repository.

## CI/CD Pipeline

GitHub Actions handles continuous integration. Every PR runs unit tests, linting, and a security vulnerability scan on the dependencies.

### Blue-Green Deployments

Production rollouts utilize a Blue-Green deployment strategy. Traffic is only routed to the new pods once the `/health` probes return 200 OK.

## Configuration & Secrets

Environment variables and API keys (e.g., Bloomberg, Alpaca) are never hardcoded. They are injected at runtime via HashiCorp Vault.

## Frontend Hosting

The Next.js application is deployed to Vercel, heavily utilizing edge caching to serve the initial React Server Components instantly worldwide.

## Networking

An NGINX Ingress Controller acts as the main reverse proxy, intelligently routing API requests to the appropriate microservices.

### WebSocket Handling

The Ingress controller is tuned specifically to maintain long-lived WebSocket connections required for live price tick streaming.

### Security (TLS)

SSL/TLS termination occurs at the AWS Application Load Balancer. All internal pod-to-pod communication is encrypted via a service mesh (Istio).

## Data Layer

The relational state (users, portfolios) is stored in a highly available Amazon Aurora PostgreSQL cluster with cross-AZ read replicas.

### Feature Caching (Redis)

A clustered Redis instance handles ephemeral caching of calculated technical indicators to avoid re-computation during the trading day.

### Time-Series Storage

The massive historical OHLCV and tick-level data is stored in AWS S3 and queried directly via Amazon Athena for research purposes.

#### Persistent Volumes

Live trading systems utilize locally attached EBS io2 Block Express volumes (via Kubernetes PVCs) for sub-millisecond IOPS.

## Network Security (VPC)

The database layer is isolated in private subnets. The Kubernetes nodes reside in separate private subnets with strict Security Groups.

## Observability

All container `stdout` and `stderr` logs are collected by Fluent Bit and forwarded to an Elasticsearch cluster (ELK stack) for centralized querying.

### APM Tracing

Datadog APM traces every request through the microservices, identifying latency bottlenecks in real-time.

### Metrics Scraping

Prometheus automatically scrapes `/metrics` endpoints across the cluster, tracking pod memory usage, API error rates, and inference times.

