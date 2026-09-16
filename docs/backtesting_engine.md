# Event-Driven Backtesting Engine

This document details the architecture and assumptions of the proprietary event-driven backtesting engine in ASHEN-VECTOR.

## Event-Driven Architecture

Unlike vectorized backtesters, our engine is purely event-driven, simulating live market microstructure to eliminate look-ahead bias.

### Event Loop

The core loop continuously processes an event queue containing `MarketEvent`, `SignalEvent`, `OrderEvent`, and `FillEvent` objects sequentially.

## Order Execution Simulation

`OrderEvent` objects are routed to a simulated exchange broker that holds them until the next valid market tick can trigger a fill.

### Latency Modeling

A synthetic microsecond delay is introduced into the matching engine to accurately simulate network latency and queue priority.

## Transaction Costs

Strict commission models are applied, factoring in SEC regulatory fees, exchange routing fees, and per-share prime broker commissions.

### Slippage Penalties

Market orders are assumed to always cross the spread. Limit orders suffer adverse selection slippage penalties based on historical depth-of-book data.

## Portfolio State & Margin

The `Portfolio` object tracks real-time cash balances, unrealized P&L, and enforces Regulation T initial and maintenance margin requirements.

