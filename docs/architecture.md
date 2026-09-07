# Architecture Documentation

This document outlines the core architecture of ASHEN-VECTOR.

## System Overview

ASHEN-VECTOR is a quantitative finance platform combining mathematical models with AI-driven consensus.

## Data Pipeline

The data pipeline relies on Qlib for robust financial dataset management and efficient retrieval.

### Feature Engineering

Features include technical indicators (RSI, MACD) and statistical metrics generated securely without look-ahead bias.

## Model Registry

The model registry tracks active models, their versions, validation metrics, and current statuses.

### Prediction Engine

Aggregates predictions from multiple base models (LightGBM, XGBoost) to form a robust consensus forecast.

## API Architecture

The FastAPI backend exposes REST endpoints categorized by stocks, predictions, live data, and validation.

### Live Market Data

Real-time inference is supported by fetching current market snapshots via yfinance and custom integrations.

## Risk Management

Calculates historical Value at Risk (VaR), Conditional VaR (CVaR), and maximum drawdowns for risk assessment.

### Portfolio Optimization

Uses modern portfolio theory to suggest optimal weights balancing expected return and risk.

## Frontend Architecture

Built with Next.js 14, Tailwind CSS, and Lucide icons, focusing on a dark 'matte black' quantitative aesthetic.

### State Management

React state is used alongside Server Components to manage real-time UI updates seamlessly.

### Component Library

Reusable components are structured under `src/components/`, including unified stock detail views and metric grids.

## Responsive Design

The UI adapts to various screen sizes while maintaining the dense, terminal-style data presentation required for finance.

## Authentication

(Reserved for future implementation of JWT-based stateless authentication flows).

### Error Handling

Backend exceptions (like `InstrumentNotFoundError`) are mapped directly to proper HTTP status codes for frontend consumption.

## Performance

Data fetching is optimized using Next.js caching where applicable, and heavy processing is offloaded to the backend.

## Testing Strategy

Includes unit testing for analytical functions and backend route validation using Pytest.

