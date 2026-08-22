---
name: portfolio-rebalancer
description: >
  Analyzes portfolio valuation, daily returns, sector concentration risk (Power, PSU, Defence),
  and underperformers. Generates strategic rebalancing plans, profit-booking recommendations, and cash
  deployment allocation. Use when evaluating portfolio health, sector concentration, rebalancing holdings,
  or deploying war chest capital.
---

# Portfolio Rebalancer

## Overview
Provides deterministic financial calculations and strategic risk management for portfolio health analysis.
It evaluates sector concentration caps (Power ≤ 30%, PSUs ≤ 30%), daily return performance against Nifty 50,
and generates structured rebalancing and capital deployment plans while maintaining strategic war chest reserves.

## When to use this skill
- When asked to analyze, review, or evaluate current portfolio holdings or overall health.
- When determining sector exposure (e.g. Power sector concentration, PSU weight).
- When planning portfolio rebalancing, profit booking, or liquidating underperforming stocks.
- When formulating capital deployment plans for liquid cash or war chest reserves.

Do **NOT** use this skill for individual stock technical breakout charting (use `technical-regime-analyzer`) or for placing brokerage orders (use `zerodha-kite-executor`).

## Inputs / Prerequisites
- Current holdings list with quantities, close prices, and current prices (fetched live via `zerodha-kite-executor` or provided in workspace/JSON).
- Benchmark performance data (Nifty 50 daily return).

## Workflow

### Step 1 — Execute Portfolio Valuation & Sector Breakdown
Run the deterministic calculator tool via bash:

```bash
python3 .agents/skills/portfolio-rebalancer/tools/portfolio_calc.py [--json-input <path>] [--nifty-return <pct>]
```

If custom holdings JSON exists in `workspace/`, pass `--json-input workspace/holdings.json`.

### Step 2 — Audit Risk & Concentration Limits
Compare output metrics against concentration limits defined in [references/portfolio-benchmarks.md](references/portfolio-benchmarks.md):
- **Power Sector Risk**: Flag if Power sector exceeds 30.0% of total portfolio value.
- **PSU Concentration Risk**: Flag if PSUs exceed 30.0% of total portfolio value.
- **Relative Benchmark Return**: Verify if `portfolio_return_pct` > `nifty_return_pct`.

### Step 3 — Flag Underperformers & Trim Candidates
Identify holdings that meet trimming criteria:
- Stock trading below 50 EMA or lagging Nifty by > 2.0% on the day.
- Over-concentrated sector positions with extended valuations.
- Positions near earnings dates (within 5 trading days).

### Step 4 — Formulate Capital Deployment & War Chest Plan
1. Calculate liquid cash available + proceeds from planned trims.
2. Reserve **15% – 20%** as strategic War Chest cash for market corrections.
3. Allocate remaining capital into under-represented, high-RS sectors (e.g., Financials, Consumer, Quality Growth) following setup criteria from `stock-picker-momentum`.

## Verification
Confirm the analysis report includes:
- [ ] Total portfolio current valuation, daily absolute change (₹), and daily return (%).
- [ ] Sector weight breakdown summing to 100%.
- [ ] Concentration warning flags for any sector > 30% or PSU > 30%.
- [ ] Benchmark comparison statement (Outperforming vs Underperforming Nifty 50).
- [ ] Explicit cash reserve allocation amount (War Chest).

## References
- [references/portfolio-benchmarks.md](references/portfolio-benchmarks.md) — Sector concentration thresholds, risk caps, and benchmark scoring rules.
