# Portfolio Manager Agent (Pi Framework)

## Overview
This repository functions as the workspace and knowledge base for the **Portfolio Manager Agent** operating on the `pi` coding agent framework.

The agent uses Engineering Capability Packages (ECPs) located in `.agents/skills/` to perform technical analysis, stock selection, portfolio rebalancing, and brokerage execution.

## Operational ECP Skills
The agent discovers and loads the following skills on demand:

1. **`portfolio-rebalancer`** (`.agents/skills/portfolio-rebalancer`)
   - Calculates portfolio valuations, daily PnL, sector weight distribution, and Nifty 50 relative returns.
   - Enforces concentration risk caps (Power ≤ 30%, PSUs ≤ 30%) and calculates liquid war chest reserves.

2. **`technical-regime-analyzer`** (`.agents/skills/technical-regime-analyzer`)
   - Evaluates Nifty 50 market regime (Trending Up, Trending Down, Sideways).
   - Computes quantified stock regime scores (0.0–1.0) and validates Break of Structure (BOS) breakouts and demand zone retracements.

3. **`stock-picker-momentum`** (`.agents/skills/stock-picker-momentum`)
   - Screens liquid NSE stocks (Nifty 50 / Nifty 100, Price > ₹100, Volume > 1M shares).
   - Enforces hard exclusion filters (pre-earnings within 5 days, recent circuit hits) and defines entry, stop-loss, and target trade plans.

4. **`zerodha-kite-executor`** (`.agents/skills/zerodha-kite-executor`)
   - Handles Zerodha Kite login status check, profile inspection, live holdings, and open orders.
   - Places market/limit trade orders and GTT downside stop-loss orders using Decimal price and quantity precision.

## Portfolio Summary (Baseline)
- **Portfolio Value**: ~₹10.53 Lakhs
- **Key Holdings**: ADANIPOWER, BEL, COCHINSHIP, ICICIBANK, NTPC, TATAPOWER, TRENT, etc.
- **Concentration Risk**: High concentration in Power sector (~53.5%) and PSUs (~59.3%).
- **Primary Rebalancing Objective**: Gradually reduce Power & PSU exposure toward ≤30% cap by liquidating underperformers on rallies and reallocating into Financials, Consumer, and Growth sectors.
