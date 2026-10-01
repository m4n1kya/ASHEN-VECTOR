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

### Rate Limiting

API endpoints are protected by a distributed Redis token-bucket algorithm, strictly limiting users to 100 requests per minute.

### Brute Force Protection

Repeated failed login attempts trigger an exponential backoff lock, ultimately resulting in a 24-hour IP ban via `fail2ban`.

## Authorization (RBAC)

A granular RBAC matrix ensures analysts can view models but cannot trigger live executions without 'Portfolio Manager' privileges.

### Single Sign-On (SSO)

Corporate authentication leverages OpenID Connect (OIDC) linked to Azure Active Directory, enforcing hardware MFA.

## Audit & Compliance

All logs stream to Datadog; sensitive PII (emails, names, IP addresses) is automatically hashed/redacted before leaving the VPC.

### Content Security Policy

The Next.js frontend delivers a strict CSP header, completely mitigating cross-site scripting (XSS) by blocking inline scripts.

### CSRF Mitigation

Authentication cookies are flagged `HttpOnly`, `Secure`, and `SameSite=Strict`, rendering Cross-Site Request Forgery impossible.

## Supply Chain Security

Dependencies are scanned daily by Snyk and GitHub Dependabot; any 'Critical' CVE immediately halts the deployment pipeline.

### Container Hardening

Microservices run on Google Distroless base images with no shell access, running strictly as a non-root `appuser`.

### Secrets Management

Environment variables never contain secrets. Applications authenticate with HashiCorp Vault at startup to retrieve ephemeral database credentials.

### Cryptographic Memory

C++ risk engine modules actively wipe private keys from RAM immediately after signing transactions using `SecureZeroMemory`.

## Offensive Security

The perimeter undergoes continuous automated pentesting, augmented by a private HackerOne bug bounty program.

### Incident Response

A formalized 4-stage playbook (Identification, Containment, Eradication, Recovery) dictates the engineering response to suspected breaches.

### Intrusion Detection Part 21

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 22

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 23

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 24

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 25

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 26

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 27

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 28

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 29

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 30

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 31

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 32

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 33

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 34

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 35

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 36

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 37

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

### Intrusion Detection Part 38

Incremental optimization to the network heuristic analysis and packet inspection ruleset.

