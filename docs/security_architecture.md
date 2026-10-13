# Security Architecture & Threat Mitigation

This document outlines the security controls, data integrity guarantees, and operational safeguards implemented across the ASHEN-VECTOR platform.

---

## 1. Defense-in-Depth Principles

ASHEN-VECTOR is architected around strict boundary validation, least-privilege execution, and deterministic error isolation between the Next.js presentation layer and the FastAPI quantitative compute engine.

### Core Security Tenets
- **Strict Schema Validation**: Every API request payload is validated through strongly typed Pydantic v2 models (`src/ashen_vector/api/schemas/`) before reaching any analytical or model execution service.
- **Input Sanitization**: Instrument symbols, date bounds, and horizon arrays are normalized and bounds-checked to prevent path traversal, command injection, or resource exhaustion.
- **Zero Secrets in Repository**: Environment-specific paths and credentials are externalized via `.env` and `pydantic-settings` (`src/ashen_vector/config/settings.py`), with `.env` strictly excluded via `.gitignore`.

---

## 2. API & Transport Layer Controls

### CORS & Origin Enforcement
Cross-Origin Resource Sharing (CORS) middleware in `src/ashen_vector/api/main.py` restricts browser-originated requests to configured frontend origins and explicitly permitted HTTP methods.

### Rate Limiting & Compute Guardrails
Long-running quantitative workloads—such as Purged Walk-Forward Validation (`/api/validation/run`) and Event-Driven Backtesting (`/api/backtest`)—are executed asynchronously via background job managers (`job_manager.py`, `validation_runner.py`), preventing synchronous worker starvation.

---

## 3. Container & Runtime Hardening

- **Non-Root Execution**: Production Docker containers execute under an unprivileged system user (`ashen`) with read-only root filesystems where applicable.
- **Dependency Pinning & Auditing**: Python (`pyproject.toml`) and Node.js (`package-lock.json`) dependencies are locked and audited via automated CI workflows.
- **Artifact Integrity**: Serialized model artifacts (`models/`) are validated via metadata checksums in the `ModelRegistry` before deserialization.
