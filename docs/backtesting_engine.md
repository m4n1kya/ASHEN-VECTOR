# Event-Driven Backtesting Engine

This document details the architecture and assumptions of the proprietary event-driven backtesting engine in ASHEN-VECTOR.

## Event-Driven Architecture

Unlike vectorized backtesters, our engine is purely event-driven, simulating live market microstructure to eliminate look-ahead bias.

### Event Loop

The core loop continuously processes an event queue containing `MarketEvent`, `SignalEvent`, `OrderEvent`, and `FillEvent` objects sequentially.

