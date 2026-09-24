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

