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

