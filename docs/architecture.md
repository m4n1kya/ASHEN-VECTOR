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

