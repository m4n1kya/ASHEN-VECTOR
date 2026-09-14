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

