# FSE Trading System Architecture

## Overview
FSE (Fully Smart Execution) is a modular crypto trading bot designed for:
- High volatility alpha coins
- Hedge mode (LONG + SHORT simultaneously)
- Grid trading + partial take-profit
- Risk-aware adaptive leverage system
- Multi-exchange execution layer

---

## Core Layers

### 1. Brain Layer
Responsible for generating trading signals.
- Input: Market data
- Output: LONG / SHORT / HEDGE / WAIT
- Includes:
  - AI predictor
  - Signal confidence scoring

---

### 2. Risk Engine
Controls whether trades are allowed.

Rules:
- Confidence threshold must be ≥ 15%
- System blocks trades if:
  - Volatility too low
  - Drawdown exceeds limit
  - Emergency stop triggered

---

### 3. Leverage Engine (Adaptive System)

Leverage is dynamically adjusted based on confidence:

| Confidence Range | Leverage |
|------------------|----------|
| 15 – 25%         | 5x       |
| 26 – 35%         | 8x       |
| 36 – 55%         | 10x      |
| 56 – 75%         | 15x      |
| 76 – 85%         | 20x      |
| 86%+             | 30x      |

Rule:
- Below 15% → NO TRADE

Optional safety layer:
- Volatility-adjusted cap reduces leverage in unstable markets

---

### 4. Execution Layer
Handles order placement:
- Binance / Bybit / OKX / KuCoin / Gate.io / MEXC / Bitget
- Forex MT5 brokers (OANDA, IC Markets, Exness, Pepperstone)

Supports:
- Market orders
- Hedge execution
- Grid execution
- Partial fills

---

### 5. Strategy Layer
Includes:
- Trend following
- Mean reversion
- Smart money structure logic
- Grid trading mode
- Hedge decision logic

---

### 6. Portfolio Layer
- Position sizing
- Capital allocation per trade
- Risk balancing per coin

---

### 7. Monitoring Layer
- Logs trades
- Tracks performance
- Handles system health checks
- Sends alerts (Telegram)

---

## Execution Flow

Market Data → Brain → Risk Engine → Strategy → Portfolio → Execution → Exchange → Monitoring
