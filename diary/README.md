# Agent Daily Diary (`diary/`)

This directory contains the daily operational diary entries maintained by the Portfolio Manager Agent.

## File Naming Convention
Files are named by ISO date: `diary/YYYY-MM-DD.md` (e.g. `diary/2026-04-20.md`).

## Standard Diary Structure
Each daily entry captures the high-level operational transcript:

```markdown
# Portfolio Manager Daily Diary — YYYY-MM-DD

## 1. Beginning of Day (BOD) Snapshot
- **Nifty 50 Market Regime**: [TRENDING_UP / TRENDING_DOWN / SIDEWAYS]
- **Nifty Technicals**: Price vs 20/50 EMA, ADX(14) level
- **Portfolio Valuation**: ₹X.XX Lakhs
- **Daily PnL / Return**: ₹X.XX (+X.XX% vs Nifty X.XX%)
- **Sector Concentration**: Power X%, PSU X%
- **Available Liquid Cash (War Chest)**: ₹X.XX Lakhs

## 2. Key Observations & Activities
- [ ] Portfolio health audit completed.
- [ ] Setup scan performed for Nifty 50/100 candidate stocks.
- [ ] Detailed research drafted in `resources/YYYY-MM-DD/<topic>.md`.

## 3. Orders & Execution
- **Orders Placed**:
  - `SYMBOL`: Side, Qty, Limit Price, Order ID
- **GTT Stop Loss Status**:
  - `SYMBOL`: Trigger Price, Limit Price, Status

## 4. End of Day (EOD) Reflection & Learnings
- Summary of daily performance and market behavior.
- Identified candidate insights to promote/distill into ECPs in `.agents/skills/`.
```
