# Sentiment Analysis and NLP Pipeline

This document outlines the architecture for ingesting and processing unstructured textual data in ASHEN-VECTOR.

## Objective

The NLP pipeline aims to extract predictive alpha from alternative data sources, capturing market sentiment before it is reflected in price action.

## SEC Filings Ingestion

A custom scraper continuously monitors the SEC EDGAR database for new 10-K, 10-Q, and 8-K filings for our investment universe.

### MD&A Extraction

Using regular expressions and HTML parsing, the pipeline extracts the critical 'Management Discussion and Analysis' section from raw filings.

