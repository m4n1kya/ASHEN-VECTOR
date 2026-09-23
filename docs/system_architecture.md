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

## Application Security

AWS WAF is deployed in front of the API Gateway, enforcing rate-limit rules and blocking common OWASP Top 10 attack vectors.

### SQL Injection Prevention

All database queries use SQLAlchemy's parameterized query engine, making raw string interpolation into SQL statements structurally impossible.

### Penetration Testing

The platform undergoes bi-annual third-party penetration tests, with Critical and High findings requiring remediation within 14 days.

### Secrets Rotation

All external API keys and database credentials are automatically rotated on a 90-day cycle via HashiCorp Vault's dynamic secrets engine.

### Container Vulnerability Scanning

Every Docker image built in CI is scanned by Trivy for known CVEs. Images with Critical vulnerabilities are blocked from deployment.

### Python Dependency Auditing

`pip-audit` runs on every pull request to detect known vulnerabilities in transitive dependencies before they enter the codebase.

## Distributed Tracing

Jaeger distributed tracing is integrated across all microservices, providing end-to-end visibility into complex multi-service request flows.

### W3C TraceContext

All services propagate trace context using the W3C TraceContext standard (`traceparent` header), ensuring compatibility with all observability tools.

### Adaptive Sampling

Jaeger uses adaptive sampling, automatically increasing the trace collection rate for slow or erroneous requests to diagnose production issues.

## Structured Logging

All services emit structured JSON logs containing a `correlation_id`, `trace_id`, `service_name`, and `severity` for precise log aggregation.

### Log Pipeline

Fluent Bit DaemonSets collect logs from all pod stdout streams, parse JSON fields, enrich with Kubernetes metadata, and forward to Elasticsearch.

### Kibana Dashboards

Real-time Kibana dashboards visualize error rates, request latencies, and model inference counts, enabling rapid incident triage.

## Alerting

Grafana AlertManager is configured with tiered PagerDuty integrations: P1 alerts (live trading failures) page on-call engineers immediately.

### Service Level Objectives

Formalized SLOs define a 99.9% API availability target and a p99 inference latency target of under 500 milliseconds within each trading day.

### Error Budget Alerts

An alert fires when the 6-hour error budget burn rate exceeds 14x the baseline, indicating a rapidly deteriorating system before the SLO window closes.

## Async Task Processing

Long-running tasks such as full model retraining and portfolio backtests are offloaded to a Celery worker fleet backed by a Redis message broker.

### Priority Queues

Celery is configured with three priority queues: `critical` (live risk recalculation), `high` (model retraining), and `low` (report generation).

### Worker Auto-Scaling

Kubernetes KEDA (Kubernetes Event-Driven Autoscaler) scales the Celery worker pool based on the Redis queue depth, from a minimum of 2 to 20 pods.

## Multi-Tier Caching

A multi-tier caching strategy reduces database load: L1 is in-process Python LRU cache, L2 is Redis, and L3 is Aurora's query result cache.

### Cache Invalidation

Feature vector caches are invalidated using a Pub/Sub notification from the FES whenever a new model input is computed for a given instrument.

### TTL Configuration

OHLCV bars are cached for 60 seconds, calculated alpha features for 30 seconds, and static reference data (e.g., sector mappings) for 24 hours.

## API Design Standards

All list endpoints implement cursor-based pagination using opaque `next_cursor` tokens, avoiding the performance issues of offset-based pagination.

### Error Response Schema

All API errors conform to the RFC 7807 'Problem Details' JSON schema, providing `type`, `title`, `status`, and `detail` fields consistently.

### API Versioning

Breaking API changes are introduced via a new URI version prefix (e.g., `/api/v2/`), with a minimum 6-month deprecation window for `/api/v1/`.

### GraphQL Research API

An internal GraphQL endpoint allows quantitative researchers to construct arbitrary, deeply nested queries across instruments and features.

## Frontend Architecture

The Next.js frontend uses Zustand for lightweight client-side state management, avoiding the complexity of Redux for simple UI state.

### Server Component Fetching

Expensive data fetches (e.g., historical performance charts) are performed in React Server Components, eliminating client-side waterfall requests.

### Build Optimization

Next.js's Turbopack bundler automatically performs code splitting and tree shaking, ensuring each page only loads the JavaScript it strictly requires.

### WebSocket Reconnection

The frontend WebSocket client implements exponential backoff with jitter for reconnection attempts, preventing thundering herd reconnections after server restarts.

### Core Web Vitals

Google Fonts are loaded using `next/font` with `font-display: swap` to eliminate layout shifts and meet the Core Web Vitals CLS threshold.

## Database Architecture

The relational schema follows Third Normal Form (3NF) strictly, decomposing redundant data into reference tables to ensure data integrity.

### Indexing Strategy

Composite B-Tree indexes on `(symbol, date)` columns eliminate full-table scans for the most frequent time-series range queries.

### Partial Indexes

Partial indexes filtered to `WHERE is_active = TRUE` reduce index sizes by 60% for queries that exclusively target the active investment universe.

### Connection Pooling (PgBouncer)

PgBouncer acts as a connection pooler in transaction pooling mode, allowing thousands of application pods to share a fixed pool of 100 database connections.

### Read Replica Routing

SQLAlchemy is configured to automatically route read-only ORM queries to the Aurora read replica, freeing the primary writer for transactional workloads.

### Table Partitioning

The `daily_prices` table is partitioned by year using PostgreSQL declarative partitioning, enabling instant purging of historical data via `DETACH PARTITION`.

## Stream Processing (Apache Flink)

Apache Flink processes the real-time Kafka event stream for stateful computations like rolling technical indicators and order book aggregations.

### Event-Time Watermarking

Flink watermarks are configured with a 5-second lateness tolerance, correctly handling late-arriving ticks from high-latency venues.

### Exactly-Once Processing

Flink's incremental checkpointing to S3 provides exactly-once processing guarantees, ensuring no tick is double-counted in rolling feature computations.

## Batch Processing (Apache Spark)

Apache Spark on Amazon EMR handles the nightly batch jobs: full covariance matrix recalculation, model retraining, and portfolio attribution.

### Airflow DAG Orchestration

All Spark batch jobs are orchestrated as Apache Airflow DAGs, providing dependency management, retry logic, and Slack failure notifications.

## Data Lakehouse (Delta Lake)

The raw and processed data lakes are built on AWS S3 with Delta Lake format, providing ACID transactions and time-travel queries for data.

### Medallion Architecture

Data flows through three layers: Bronze (raw vendor data), Silver (cleaned and validated data), and Gold (feature-engineered, model-ready datasets).

### Z-Order Optimization

Delta Lake tables are Z-ordered on `(symbol, date)` columns to co-locate related data on the same Parquet files, drastically reducing I/O.

### Table Maintenance

Automated Airflow DAGs run Delta Lake `VACUUM` and `OPTIMIZE` commands nightly to manage small file proliferation and reclaim storage.

## Infrastructure as Code (Terraform)

Every AWS resource is provisioned via Terraform, with state stored in S3 and locked via DynamoDB to prevent concurrent state modifications.

### Module Structure

Terraform modules are structured hierarchically: `modules/networking`, `modules/compute`, `modules/database`, and `modules/monitoring` for reusability.

### Remote Execution

All `terraform plan` and `terraform apply` executions run in Terraform Cloud, ensuring a consistent environment and providing a full audit log.

## GitOps Deployment (ArgoCD)

ArgoCD monitors the `k8s-manifests` Git repository and automatically synchronizes the Kubernetes cluster state to match the declared configuration.

### Application Sets

ArgoCD Application Sets template a single application definition across `dev`, `staging`, and `prod` environments using Git branch selectors.

### Kustomize Overlays

Environment-specific differences (replica counts, resource limits, feature flags) are managed via Kustomize overlays on a shared base configuration.

### Resource Quotas

Kubernetes Resource Quotas are applied at the namespace level, preventing a runaway ML training job from starving live trading pods of CPU and memory.

### Vertical Pod Autoscaler

The VPA automatically adjusts the memory requests of ML inference pods based on historical usage, eliminating manual resource tuning.

### Pod Disruption Budgets

Pod Disruption Budgets (PDB) guarantee a minimum of 2 replicas for the OMS and RMS services during voluntary node drains or cluster upgrades.

## Disaster Recovery Strategy

Recovery Time Objective (RTO) is set at 15 minutes and Recovery Point Objective (RPO) at 60 seconds for the live trading cluster.

### Failover Runbook

The documented runbook for primary region failover involves three steps: promote Aurora standby, update Route 53 DNS records, and resume Kubernetes deployments.

### Chaos Engineering

Controlled Chaos Monkey experiments are run monthly in the staging environment, validating that circuit breakers and failover mechanisms operate as designed.

## Capacity Planning

Load testing via Locust simulates peak market-open order flow to validate that the platform sustains 10,000 concurrent API requests without degradation.

### Inference Latency Benchmarks

Benchmarking on production hardware confirms a p50 inference latency of 12ms and a p99 of 87ms for the full 7-model ensemble.

### Placement Groups

Latency-sensitive inference and OMS pods are co-located within a single AWS Cluster Placement Group to minimize cross-rack network hops.

### Kernel-Bypass Networking

For the highest-frequency tick ingestion path, DPDK (Data Plane Development Kit) bypasses the Linux kernel network stack for sub-10 microsecond latency.

