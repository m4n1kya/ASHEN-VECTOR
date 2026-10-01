# Security Architecture

This document outlines the zero-trust security model protecting the ASHEN-VECTOR proprietary algorithms and user data.

## Zero-Trust Perimeter

All internal microservices strictly authenticate via mTLS; no internal network segment is considered 'trusted' by default.

### JWT Authentication

User sessions are maintained via short-lived JWTs (15 min expiry) signed with RS256, utilizing an asymmetric public/private key pair.

