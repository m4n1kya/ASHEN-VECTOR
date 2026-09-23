# ASHEN-VECTOR System Architecture

This living document is the definitive reference for the holistic architecture of the ASHEN-VECTOR quantitative trading platform.

## Architectural Philosophy

ASHEN-VECTOR is designed around three non-negotiable principles: correctness of computation, resilience under failure, and extreme operational transparency.

## Microservices Decomposition

The monolithic research prototype was decomposed into eight autonomous microservices, each owning its own data store and deployment lifecycle.

### Market Data Service (MDS)

The MDS is the sole owner of raw market data ingestion, responsible for normalizing feeds from multiple providers into a canonical internal format.

