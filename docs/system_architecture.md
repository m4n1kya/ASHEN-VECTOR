# ASHEN-VECTOR System Architecture

This living document is the definitive reference for the holistic architecture of the ASHEN-VECTOR quantitative trading platform.

## Architectural Philosophy

ASHEN-VECTOR is designed around three non-negotiable principles: correctness of computation, resilience under failure, and extreme operational transparency.

## Microservices Decomposition

The monolithic research prototype was decomposed into eight autonomous microservices, each owning its own data store and deployment lifecycle.

### Market Data Service (MDS)

The MDS is the sole owner of raw market data ingestion, responsible for normalizing feeds from multiple providers into a canonical internal format.

### Feature Engineering Service (FES)

The FES subscribes to the MDS event stream and produces a continuously updated, point-in-time correct feature vector for each instrument.

### Model Inference Service (MIS)

The MIS is intentionally stateless, loading serialized ONNX models from a shared artifact store at startup and serving predictions via gRPC.

### Risk Management Service (RMS)

No order may be generated without first receiving a synchronous approval from the RMS, which validates every proposed position against portfolio-level limits.

### Order Management Service (OMS)

The OMS implements a strict finite state machine tracking every order through PENDING, SUBMITTED, PARTIAL_FILL, FILLED, and CANCELLED states.

### Portfolio Accounting Service (PAS)

The PAS is the immutable source of truth for all positions, cash balances, and realized P&L, implemented as an append-only ledger.

### Research & Backtesting Service (RBS)

The RBS is air-gapped from the live trading cluster, running on a separate compute pool with zero access to live order routing endpoints.

### API Gateway Service (AGS)

The AGS is the single public-facing entry point, aggregating responses from multiple internal microservices for the Next.js frontend.

## Inter-Service Communication

Asynchronous communication between services is exclusively mediated through Apache Kafka, ensuring loose coupling and fault isolation.

### Topic Naming Conventions

Kafka topics follow the schema `{env}.{domain}.{entity}.{version}` (e.g., `prod.market.ohlcv.v3`) to enforce discoverability and schema evolution.

### Synchronous gRPC

For latency-critical synchronous calls (e.g., risk checks), services communicate via gRPC with Protocol Buffer schemas, reducing serialization overhead.

## Service Mesh (Istio)

Istio is deployed as the service mesh layer, providing automatic mTLS encryption, circuit breaking, and distributed tracing between all pods.

### Circuit Breaker Pattern

Istio circuit breakers are configured to trip after 3 consecutive 500-series errors, immediately routing traffic to fallback handlers.

### Sidecar Proxies (Envoy)

Envoy sidecar proxies are automatically injected into every pod, collecting granular telemetry on request rates, latency, and error ratios.

## Event Sourcing

The Order Management Service state is reconstructed exclusively from an append-only stream of domain events, enabling perfect auditability.

### Command Query Responsibility Segregation (CQRS)

Write operations (order placement) are handled by a command handler, while read operations (portfolio dashboard) query a separate, denormalized read model.

### Event Store Schema

Each event contains a globally unique `event_id`, a `aggregate_id`, a monotonically increasing `sequence_number`, and an ISO 8601 `recorded_at` timestamp.

## Distributed Transactions (Saga Pattern)

The multi-step trade placement workflow (risk check -> order creation -> execution -> accounting) is orchestrated as a saga with compensating transactions.

### Choreography Saga

The trade settlement saga uses choreography, where each service reacts to domain events and emits new events, eliminating a central orchestrator bottleneck.

### Compensating Transactions

If the accounting service fails to record a fill, a compensating `FILL_REVERSAL` event is emitted, triggering an automated reconciliation workflow.

## Idempotency

All Kafka consumers implement idempotent processing by storing processed `event_id` values in Redis, safely tolerating at-least-once message delivery.

## Architectural Decision Records

All significant architectural decisions are documented as ADRs in `docs/adr/`, providing historical context for future engineers.

### ADR-001: Kafka over RabbitMQ

Kafka was selected over RabbitMQ primarily for its immutable log retention, enabling replay-based backtesting of live order flow.

### ADR-002: FastAPI over Django REST Framework

FastAPI was selected for its native async support and automatic OpenAPI schema generation, critical for our high-concurrency inference endpoints.

### ADR-003: ONNX Runtime for Production Serving

ONNX Runtime was selected to eliminate the Python GIL bottleneck during parallel model inference, achieving sub-10ms p99 latency.

### ADR-004: Next.js 14 App Router

Next.js 14's App Router was selected for its support for React Server Components, dramatically reducing the JavaScript payload sent to clients.

### ADR-005: TimescaleDB for Aggregated Metrics

TimescaleDB was selected over InfluxDB for storing pre-aggregated OHLCV bars due to its PostgreSQL compatibility and mature SQL support.

## High Availability Architecture

The live trading cluster is deployed in an active-passive multi-region configuration across AWS us-east-1 (primary) and eu-west-1 (standby).

### Database Failover

Amazon Aurora automatically promotes the standby read replica to primary within 30 seconds, without requiring manual intervention.

### Health Check Probes

Kubernetes liveness probes restart crashed pods while readiness probes prevent traffic from reaching pods that are still warming up their ONNX models.

### Rolling Restarts

Kubernetes rolling update strategy ensures at least 2 replicas of each service remain available at all times during a deployment rollout.

## Network Topology

The AWS VPC is segmented into three tiers: public (load balancers), private application (Kubernetes nodes), and isolated data (RDS, ElastiCache).

### Bastion Host Access

Engineers access the private cluster exclusively via a hardened Bastion Host, with all SSH sessions logged and audited to CloudTrail.

### Service Discovery

Kubernetes CoreDNS provides internal service discovery, allowing services to reach each other via stable DNS names regardless of pod IP changes.

### NAT Gateway

Private application pods route outbound internet requests (e.g., to Bloomberg API) through a managed NAT Gateway, masking internal IPs.

### Least Privilege Security Groups

AWS Security Groups implement a strict allow-list model; the Postgres port 5432 is only reachable from the application subnet CIDR, not the internet.

