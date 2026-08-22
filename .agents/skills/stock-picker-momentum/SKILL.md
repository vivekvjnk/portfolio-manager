---
name: stock-picker-momentum
description: >
  Filters market universe (NIFTY 50 / NIFTY 100), applies liquidity guidelines (Price > 100 INR,
  Volume > 1M, circuit/earnings exclusion), and selects high-momentum pullback continuation setups.
  Use when selecting candidate stocks, finding swing trade setups, or screening momentum opportunities.
---

# Stock Picker Momentum

## Overview
Identifies high-momentum, structure-aligned stock picks in the Indian equity market (NSE).
It applies strict universe filters (Nifty 50/100, Price > ₹100, Volume > 1M), excludes high-risk events (earnings within 5 days, recent circuit hits), and picks pullback continuation opportunities after confirmed Break of Structure (BOS) events.

## When to use this skill
- When asked to pick, suggest, or recommend stocks for trading or investment.
- When searching for high-momentum swing trade opportunities.
- When building a watchlist of structure-aligned stocks.
- When evaluating setup quality against liquidity and earnings exclusion filters.

Do **NOT** use this skill for executing brokerage orders (use `zerodha-kite-executor`) or portfolio allocation calculation (use `portfolio-rebalancer`).

## Inputs / Prerequisites
- Daily market scanner output or stock ticker list.
- Earnings release calendar and recent 10-day price history.

## Workflow

### Step 1 — Apply Universe & Liquidity Filters
Verify target stock meets all liquidity criteria per [references/universe-filters.md](references/universe-filters.md):
- [ ] Part of NIFTY 50 or NIFTY 100 index (Cash segment).
- [ ] Stock price > ₹100.
- [ ] 20-day Average Daily Volume > 1,000,000 shares.

### Step 2 — Apply Hard Exclusion Filters
REJECT any stock that triggers an exclusion rule:
- [ ] Earnings release scheduled within 5 trading days.
- [ ] Upper or lower circuit hit in the last 10 trading days.
- [ ] ADX(14) < 20 or price squeezed between 20 EMA and 50 EMA.

### Step 3 — Verify Technical Structure & Setup
Pass candidate stock through `technical-regime-analyzer`:
1. Confirm Nifty 50 is in **Trending Up** regime.
2. Confirm stock is forming higher highs and higher lows above 20 & 50 EMAs with ADX > 25.
3. Confirm valid BOS breakout and clean retracement into demand zone.

### Step 4 — Define Trade Plan & Position Limits
Construct the exact trade parameter plan:
- **Entry Price**: Confirmed bullish candle close above previous candle high in demand zone.
- **Stop Loss**: Below demand zone low $- 0.3\%$ buffer.
- **Targets**:
  - Target 1 (1:1 R:R): Exit 50% position, move SL to breakeven.
  - Target 2 (1:2 R:R): Exit remaining 50% or trail with 20 EMA.
- **Concentration Check**: Verify new entry does not push sector weight over 30%.

## Verification
Confirm stock picker output includes:
- [ ] Liquidity verification (Price > ₹100, Vol > 1M).
- [ ] Earnings/Circuit exclusion confirmation.
- [ ] Regime score verification (≥ 0.60).
- [ ] Specific Entry Price, Stop Loss, Target 1 (1:1), and Target 2 (1:2) values.

## References
- [references/universe-filters.md](references/universe-filters.md) — Universe rules, earnings exclusion specs, and R:R target rules.
