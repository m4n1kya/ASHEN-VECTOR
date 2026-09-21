# Data Governance and Lineage Framework

This document outlines the rigorous data management protocols enforcing quality and compliance across ASHEN-VECTOR.

## Objective

In quantitative finance, 'garbage in, garbage out' is an existential threat. This framework guarantees pristine, point-in-time accurate data.

## Data Catalog

We maintain a centralized Data Catalog acting as the single source of truth for all structured and unstructured datasets.

### Metadata Schemas

Every dataset is registered with strict metadata schemas, defining the granularity (tick, minute, daily), provider, and update frequency.

### Data Discovery

The catalog is indexed using an Amundsen-style interface, allowing quants to rapidly search and discover alternative datasets for alpha research.

## Data Quality Engineering

Automated quality gates are enforced using the Great Expectations framework before any data enters the bronze lake.

### Row-Level Validation

Strict assertions ensure OHLCV bars do not contain missing minutes during core trading hours and that High >= Low always.

### Distribution Checks

Incoming ticks are evaluated against historical distributions to flag 'fat-finger' errors or corrupt feeds immediately.

### Corporate Action Anomalies

Machine learning anomaly detectors flag suspicious corporate actions (e.g., a 1000:1 split) for manual review by a data engineer.

## Point-In-Time Architecture

Financial data is frequently restated (e.g., earnings revisions). The database strictly records both `knowledge_time` and `effective_time`.

### As-Of Joins

All historical feature generation utilizes exact 'As-Of' joins, guaranteeing that models are only trained on data known at that exact microsecond.

## Data Lineage

Data lineage is tracked comprehensively from raw vendor API to final model inference using Apache Atlas.

### Transformation Tracking

Every pandas/spark transformation applied during feature engineering is logged, creating a fully reproducible directed acyclic graph (DAG).

### Feature Provenance

If a model behaves erratically, quants can trace any final input feature directly back to the raw JSON payload provided by the vendor.

## Schema Registry

All real-time streaming data flows through Kafka topics governed by a strict Confluent Schema Registry.

### Protobuf Serialization

Market data ticks are serialized using Protocol Buffers (Protobuf) to minimize bandwidth and eliminate JSON parsing overhead.

### Schema Evolution

The registry enforces backward compatibility; vendors cannot drop fields or change data types without creating a new versioned topic.

## Feature Store Integration

Calculated alphas and technical indicators are materialized into a centralized Feature Store (Feast architecture).

### Offline vs Online Stores

The offline store (Parquet/S3) provides massive throughput for model training, while the online store (Redis) provides sub-millisecond serving latency.

### Online Caching

The online store utilizes aggressive LRU eviction policies, guaranteeing the inference engine never waits for disk I/O.

### Training Correctness

The Feature Store SDK automatically constructs point-in-time correct training datasets, eliminating complex SQL logic from the quant research process.

