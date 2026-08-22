---
name: technical-regime-analyzer
description: >
  Evaluates daily market regimes (Nifty 50), technical price structures, Break of Structure (BOS) events,
  3-candle swing pivots, ATR demand zones, 20/50 EMAs, and ADX trend strength. Use when performing
  structure-based technical analysis, evaluating market regime filters, or scoring trade setups.
---

# Technical Regime Analyzer

## Overview
Executes deterministic technical analysis on the Daily timeframe for Indian equity markets (NSE/BSE).
It enforces market-level regime filters (Nifty 20/50 EMA & ADX > 25), computes quantified stock regime scores (0.0–1.0), validates Break of Structure (BOS) breakouts, and evaluates demand zone retracement quality.

## When to use this skill
- When analyzing market regime or overall Nifty technical trend.
- When performing structure-based technical analysis on a specific stock.
- When evaluating Break of Structure (BOS) breakouts or demand zones.
- When scoring setup quality before approving trade execution.

Do **NOT** use this skill for fundamental valuation (use `stock-picker-momentum` or `portfolio-rebalancer`) or for placing GTT orders (use `zerodha-kite-executor`).

## Inputs / Prerequisites
- Daily OHLCV data for Nifty 50 and target stocks.
- Minimum 60 daily candles required to compute 50 EMA, 14 ADX, and 14 ATR accurately.

## Workflow

### Step 1 — Verify Market Regime Filter (NIFTY 50 Hard Rule)
Before analyzing any long setups, verify Nifty 50 daily status:
- **Trending Up**: Nifty > 20 EMA and 50 EMA, ADX > 25 → Proceed with long analysis.
- **Trending Down**: Nifty < 20 EMA and 50 EMA, ADX > 25 → **HARD STOP: No long trades permitted.**
- **Sideways**: Nifty between EMAs or ADX < 20 → Defensive mode; require higher regime score.

### Step 2 — Run Technical Indicators Script
Execute `tools/ta_indicators.py` via bash on historical price JSON:

```bash
python3 .agents/skills/technical-regime-analyzer/tools/ta_indicators.py --json-input <ohlcv.json> --symbol <SYMBOL>
```

### Step 3 — Compute Quantified Regime Score
Calculate the 4-part Regime Score per [references/regime-scoring-rubric.md](references/regime-scoring-rubric.md):
- Market Trend Alignment (0.0 / 0.5 / 1.0)
- Stock ADX Strength (0.0 / 0.5 / 1.0)
- Stock EMA Alignment (0.0 / 0.5 / 1.0)
- Sector Relative Strength (0.0 / 0.5 / 1.0)

**Threshold**: Minimum **0.60 required** for trade approval.

### Step 4 — Validate Break of Structure (BOS) & Demand Zone
1. Confirm 3-candle pivot swing high price.
2. Confirm breakout candle meets all 3 criteria:
   - Body $\ge 60\%$ of candle range.
   - Range $\ge 1.0 \times \text{ATR}(14)$.
   - Volume $\ge 1.5 \times$ 20-day average volume.
3. Identify demand zone (last bearish candle before breakout) and confirm width $\le 1.5 \times \text{ATR}(14)$.

## Verification
Confirm the technical analysis output includes:
- [ ] Explicit Market Regime state (Trending Up, Trending Down, or Sideways).
- [ ] 20 EMA, 50 EMA, ADX(14), and ATR(14) values.
- [ ] Quantified Regime Score (≥ 0.60 check).
- [ ] BOS verification checklist status (Body %, Range/ATR, Volume multiplier).
- [ ] Demand zone price boundary and stop-loss level.

## References
- [references/regime-scoring-rubric.md](references/regime-scoring-rubric.md) — Regime scoring math, 3-candle pivot rules, and demand zone specifications.
