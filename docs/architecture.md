
# FSE Trading Bot Architecture

## 1. Overview
FSE (Financial Smart Engine) is a modular, multi-market AI trading system designed for scalability and safety.

- **Market Support:** - **Crypto:** Binance, Bybit, OKX, KuCoin, Gate.io, MEXC, Bitget.
  - **Forex:** MT5, OANDA, IC Markets, Pepperstone, Exness.
  - **Future Assets:** Indices, Commodities (Gold/Oil/Silver), Stocks.
- **Trading Modes:** Long/Short/Hedge, Grid Trading.
- **Intelligence:** AI-driven signal generation, risk-based leverage scaling.

---

## 2. Core Modules

### 2.1 Brain Layer (AI Engine)
The central intelligence hub responsible for market analysis and decision-making.
- **Functions:** Market prediction, Signal generation (LONG/SHORT/HEDGE), Confidence scoring.
- **Output:** ```json
  {
    "signal": "LONG",
    "confidence": 78
  }
