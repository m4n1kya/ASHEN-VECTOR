# Backend Testing Framework

This document outlines the rigorous testing methodology ensuring zero regressions in the core ASHEN-VECTOR backend services.

## Pytest Architecture

The backend heavily utilizes `pytest` with a deeply nested hierarchy of fixtures defined in `conftest.py` to provide reproducible test states.

## Unit Testing

Pure mathematical functions (e.g., VaR calculation, EWMA smoothing) are tested in strict isolation without touching the disk or network.

