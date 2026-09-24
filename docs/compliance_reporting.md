# Regulatory Compliance and Reporting Framework

This document outlines the compliance architecture ensuring ASHEN-VECTOR operates within all applicable financial regulations.

## MiFID II Best Execution

All trades are evaluated against MiFID II best execution standards, with a quarterly RTS 27 report generated automatically from the TCA database.

## Market Access Controls (SEC 15c3-5)

Pre-trade risk checks enforce hard limits on order size, notional value, and aggregate daily P&L loss thresholds as mandated by SEC Rule 15c3-5.

## Suspicious Activity Reporting

An automated surveillance module flags unusual trading patterns (e.g., front-running indicators) and drafts SAR filings for compliance officer review.

## Position Limit Monitoring

The RMS monitors CFTC-mandated speculative position limits for all futures contracts, issuing alerts at 80% utilization and hard stops at 100%.

## Wash Trade Prevention

An algorithmic check prevents the OMS from simultaneously submitting buy and sell orders in the same instrument from the same account within a 60-second window.

## EOD Reconciliation

An automated reconciliation job runs at 6 PM ET daily, comparing the internal Portfolio Accounting Service records against the prime broker's official statements.

## P&L Attribution Reporting

A nightly Airflow DAG generates a full P&L attribution report decomposing daily returns into alpha, beta, transaction costs, and financing charges.

## Form PF Reporting

Quarterly Form PF data (aggregate AUM, leverage, portfolio liquidity profile) is aggregated from the PAS and formatted for SEC submission.

## Audit Log Immutability

All trading system audit logs are written to an append-only AWS S3 bucket with Object Lock enabled, guaranteeing immutability for the 7-year regulatory retention period.

## Disaster Recovery Compliance

Semi-annual disaster recovery tests are formally documented and signed off by the CCO, satisfying both SEC and FINRA operational resilience requirements.

