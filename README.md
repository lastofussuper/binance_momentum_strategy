# Crypto Momentum Strategy & Backtesting System

## Overview

This project implements a modular, data-driven trading system for cryptocurrency markets using Binance API data. It is designed to simulate a realistic research and backtesting workflow, including data ingestion, feature engineering, signal generation, and performance evaluation.

The system emphasizes clean architecture, reproducibility, and extensibility, reflecting real-world quantitative research and data platform design.

---

## Key Features

### 📊 Data Ingestion
- Fetches historical market data from Binance API
- Supports configurable symbols, intervals, and lookback windows
- Structured data storage for downstream processing

### ⚙️ Feature Engineering
- Computes momentum-based indicators from price data
- Supports configurable lookback periods
- Modular feature pipeline for easy extension

### 📈 Strategy Engine
- Implements momentum-based trading logic
- Signal generation based on configurable thresholds and parameters
- Supports long-only strategy (extendable to long/short)

### 🔁 Backtesting Framework
- Simulates trades based on generated signals
- Tracks positions, PnL, and capital over time
- Supports configurable assumptions (capital, execution logic)

### 📉 Performance Analysis
- Calculates key metrics:
  - Returns
  - Drawdowns
  - Risk-adjusted performance
- Generates outputs for further analysis and reporting

---

## Project Structure

