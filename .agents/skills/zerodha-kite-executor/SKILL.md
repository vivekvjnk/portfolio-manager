---
name: zerodha-kite-executor
description: >
  Manages Zerodha Kite brokerage operations including checking authentication status, fetching user profile,
  holdings, open orders, and placing validated trade orders or GTT (Good Till Triggered) downside stop-loss orders.
  Use when authenticating with Zerodha, inspecting account status/holdings, or placing trade/GTT orders.
---

# Zerodha Kite Executor

## Overview
Provides executable order placement and account inspection capabilities for Zerodha Kite.
It enforces Decimal precision for prices and quantities, position sizing limits, and downside protection via GTT (Good Till Triggered) single and OCO trigger orders.

## When to use this skill
- When inspecting account status, profile, or current holdings from Zerodha.
- When placing new buy or sell trade orders.
- When placing GTT downside stop-loss orders or profit-target triggers.
- When verifying open order statuses or trigger statuses.

Do **NOT** use this skill for stock setup analysis (use `stock-picker-momentum`) or technical regime scoring (use `technical-regime-analyzer`).

## Inputs / Prerequisites
- Active Zerodha Kite session token or environment credentials (`KITE_API_KEY`, `KITE_ACCESS_TOKEN`).
- Exact Decimal price and quantity values calculated from risk management rules.

## Workflow

### Step 1 — Check Authentication & Account Status
Execute status check via bash:

```bash
python3 .agents/skills/zerodha-kite-executor/tools/kite_cli.py status
```

If unauthenticated, direct user to authenticate or check environment credentials.

### Step 2 — Fetch Live Holdings & Open Orders
Fetch current positions before opening new orders:

```bash
python3 .agents/skills/zerodha-kite-executor/tools/kite_cli.py holdings
```

Verify existing quantity and exposure to avoid over-concentration or duplicate order placement.

### Step 3 — Validate Order Parameters
Verify trade against risk parameters per [references/gtt-order-specs.md](references/gtt-order-specs.md):
- Confirm price is formatted to nearest ₹0.05 tick size.
- Confirm quantity is a positive integer.
- For SELL Stop Loss GTT: Ensure Limit Price is $0.1\% - 0.2\%$ below Trigger Price to guarantee fill.

### Step 4 — Execute Order / Place GTT
For regular orders:
```bash
python3 .agents/skills/zerodha-kite-executor/tools/kite_cli.py place-order --symbol <SYMBOL> --side <BUY|SELL> --quantity <QTY> --price <PRICE>
```

For GTT Stop Loss orders:
```bash
python3 .agents/skills/zerodha-kite-executor/tools/kite_cli.py place-gtt --symbol <SYMBOL> --last-price <LTP> --trigger-price <TRIG_PRICE> --limit-price <LIMIT_PRICE> --quantity <QTY> --side SELL
```

## Verification
Confirm execution response includes:
- [ ] Valid `order_id` or `trigger_id`.
- [ ] Confirmed trading symbol, exchange, and side (BUY/SELL).
- [ ] Exact Decimal price and quantity matching request.
- [ ] Confirmation message logged to execution history.

## References
- [references/gtt-order-specs.md](references/gtt-order-specs.md) — GTT trigger types, tick size rules, slippage buffers, and validation rules.
