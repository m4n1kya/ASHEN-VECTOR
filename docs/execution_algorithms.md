# Trade Execution Algorithms

This document outlines the advanced algorithmic execution strategies used to minimize market impact in ASHEN-VECTOR.

## Objective

Theoretical alpha is useless if destroyed by execution slippage. Our execution layer systematically disguises large institutional block trades.

## TWAP Execution

The Time-Weighted Average Price (TWAP) algorithm breaks large parent orders into smaller child orders, executing evenly over a specified time horizon.

## VWAP Execution

The Volume-Weighted Average Price (VWAP) algorithm dynamically adjusts child order sizing to match historical U-shaped volume profiles.

## POV Execution

The Percentage of Volume (POV) algorithm guarantees that we never constitute more than 5% of the trailing 5-minute trading volume to avoid detection.

