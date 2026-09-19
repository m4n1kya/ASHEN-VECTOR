# Sentiment Analysis and NLP Pipeline

This document outlines the architecture for ingesting and processing unstructured textual data in ASHEN-VECTOR.

## Objective

The NLP pipeline aims to extract predictive alpha from alternative data sources, capturing market sentiment before it is reflected in price action.

## SEC Filings Ingestion

A custom scraper continuously monitors the SEC EDGAR database for new 10-K, 10-Q, and 8-K filings for our investment universe.

### MD&A Extraction

Using regular expressions and HTML parsing, the pipeline extracts the critical 'Management Discussion and Analysis' section from raw filings.

## Social Media Firehose

We ingest real-time social sentiment via the Twitter/X Enterprise Firehose, filtering for cashtags and relevant financial keywords.

### Bot Filtering

A heuristic filter discards tweets containing excessive emojis, known pump-and-dump keywords, or originating from accounts with high bot-probability scores.

## News Wire Ingestion

Live headlines and article bodies are streamed directly from Bloomberg and Reuters RSS feeds and premium APIs.

## Earnings Call Transcripts

Audio streams of quarterly earnings calls are passed through OpenAI's Whisper model to generate highly accurate, time-stamped text transcripts.

### Forward-Looking Statements

A Named Entity Recognition (NER) model identifies 'forward-looking statements', isolating management guidance from historical performance recaps.

## FinBERT Integration

We utilize FinBERT, a pre-trained NLP model specifically fine-tuned on corporate reports, earnings calls, and financial news.

### Tokenization & Batching

Incoming text is tokenized into 512-word chunks and dynamically batched for high-throughput inference on NVIDIA A100 GPUs.

## Sentiment Scoring

For each text chunk, FinBERT outputs a softmax probability distribution across three classes: Positive, Negative, and Neutral.

### Dense Embeddings

Beyond raw sentiment, the pipeline extracts the 768-dimensional pooled output vector from the transformer to capture deep semantic meaning.

## Ticker Aggregation

Sentiment scores are aggregated daily at the ticker level using a volume-weighted average of the underlying news and social mentions.

### Sentiment Smoothing

An Exponential Moving Average (EMA) is applied to the raw daily sentiment scores to reduce noise and identify sustained shifts in narrative.

## Sentiment Divergence

The system calculates a 'Divergence Score', triggering alerts when positive sentiment surges while the underlying asset price is declining.

## Dimensionality Reduction (UMAP)

To prevent the curse of dimensionality, the 768-dimensional embeddings are reduced to 16 principal components using UMAP before entering the predictive models.

## Feature Store Integration

The processed sentiment scores and reduced embeddings are written directly to the Redis feature store for instant access during inference.

