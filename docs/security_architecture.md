# Security Architecture

This document outlines the zero-trust security model protecting the ASHEN-VECTOR proprietary algorithms and user data.

## Zero-Trust Perimeter

All internal microservices strictly authenticate via mTLS; no internal network segment is considered 'trusted' by default.

### JWT Authentication

User sessions are maintained via short-lived JWTs (15 min expiry) signed with RS256, utilizing an asymmetric public/private key pair.

### Refresh Token Rotation

Refresh tokens are strictly single-use and cryptographically bound to the device fingerprint to prevent session hijacking.

## Data at Rest

All PostgreSQL volumes and S3 buckets are encrypted at rest using AES-256-GCM with keys managed by AWS KMS.

## Data in Transit

The API Gateway strictly enforces TLS 1.3, dropping older protocols and weak cipher suites to prevent downgrade attacks.

### WAF Configuration

Cloudflare WAF is configured with OWASP Top 10 managed rulesets to automatically block SQLi, XSS, and LFI attempts at the edge.

