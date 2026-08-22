---
name: zerodha-kite-executor
description: >
  Manages Zerodha Kite brokerage operations including checking authentication status, fetching user profile,
  live holdings, open orders, and placing validated trade orders or GTT (Good Till Triggered) downside stop-loss orders.
  Use when authenticating with Zerodha, inspecting account status/holdings, or placing trade/GTT orders.
---

# Zerodha Kite Executor

## Overview
Provides executable order placement and account inspection capabilities for Zerodha Kite via the Zerodha Kite MCP Server (`https://mcp.kite.trade/mcp`).
It enforces Decimal precision for prices and quantities, persistent session polling during OAuth authorization, and downside protection via GTT (Good Till Triggered) trigger orders.

## When to use this skill
- When authenticating with Zerodha Kite to access live account data.
- When inspecting real-time holdings, positions, user profile, or open orders from Zerodha.
- When placing new buy or sell trade orders.
- When placing GTT downside stop-loss orders or profit-target triggers.
- When verifying open order statuses or trigger statuses.

Do **NOT** use this skill for stock setup analysis (use `stock-picker-momentum`) or technical regime scoring (use `technical-regime-analyzer`).

## Inputs / Prerequisites
- Zerodha Kite MCP Server integration (`https://mcp.kite.trade/mcp` via `npx -y mcp-remote https://mcp.kite.trade/mcp`).
- Active browser session for OAuth login & 2FA/TOTP authorization.

---

## 🔑 Critical Architectural Discovery: MCP Session Lifecycle

`npx -y mcp-remote https://mcp.kite.trade/mcp` establishes a **connection-bound SSE/HTTP transport session**. 

* **The Subprocess Pitfall**: Launching short-lived CLI calls in separate subprocesses (e.g., running `kite_cli.py login` then exiting, and later running `kite_cli.py holdings`) opens a **new, unauthenticated session ID** on `mcp.kite.trade` for each call. The second process fails with `"Please log in first using the login tool"`.
* **The Persistent Connection Solution**: To authenticate and retrieve account data, a **single persistent Python process** must invoke `login`, write the session-bound OAuth URL, and **maintain the `ClientSession` open in a polling loop** while the user completes browser authorization. Once approved, the active session receives authorization state and immediately fetches account holdings/positions.

---

## Workflow

### Step 1 — Persistent Authentication & Data Sync

1. **Launch Persistent Sync Process in Background**:
   ```bash
   python3 .agents/skills/zerodha-kite-executor/tools/fetch_live_holdings.py > workspace/auth.log 2>&1 &
   sleep 5
   cat workspace/login_info.json
   ```

2. **Present Authorization URL to User**:
   Read `workspace/login_info.json` to extract the session-bound OAuth URL and display the mandatory AI risk disclaimer:
   
   > ⚠️ **WARNING: AI systems are unpredictable and non-deterministic. By continuing, you agree to interact with your Zerodha account via AI at your own risk.**
   > 
   > Please authorize access via this link: `https://mcp.kite.trade/authorize?session_id=...`

3. **Verify Authentication & Read Live Holdings**:
   While the user logs in via browser, `fetch_live_holdings.py` polls `get_profile` every 3 seconds on the active connection. Once approved, it automatically saves:
   * `workspace/live_holdings.json` — Live account holdings.
   * `workspace/live_positions.json` — Intraday and derivative positions.
   * `workspace/live_profile.json` — Account profile details.
   * `workspace/login_info.json` — Status updated to `"authenticated"`.

   Verify completion:
   ```bash
   cat workspace/login_info.json
   cat workspace/live_holdings.json
   ```

---

### Step 2 — Feed Live Data into Portfolio Analytics
Pass the synchronized holdings JSON into portfolio rebalancing tools:

```bash
python3 .agents/skills/portfolio-rebalancer/tools/portfolio_calc.py --json-input workspace/live_holdings.json
```

---

### Step 3 — Order Placement & GTT Triggers

Verify trade against risk parameters per [references/gtt-order-specs.md](references/gtt-order-specs.md):
- Confirm price is formatted to nearest ₹0.05 tick size.
- Confirm quantity is a positive integer.
- For SELL Stop Loss GTT: Ensure Limit Price is $0.1\% - 0.2\%$ below Trigger Price to guarantee fill.

For regular orders:
```bash
python3 .agents/skills/zerodha-kite-executor/tools/kite_cli.py place-order --symbol <SYMBOL> --side <BUY|SELL> --quantity <QTY> --price <PRICE>
```

For GTT Stop Loss orders:
```bash
python3 .agents/skills/zerodha-kite-executor/tools/kite_cli.py place-gtt --symbol <SYMBOL> --last-price <LTP> --trigger-price <TRIG_PRICE> --limit-price <LIMIT_PRICE> --quantity <QTY> --side SELL
```

---

## Verification Checklist
Confirm authentication and execution response includes:
- [ ] Active background worker (`fetch_live_holdings.py`) maintaining SSE transport.
- [ ] Live holdings successfully downloaded to `workspace/live_holdings.json`.
- [ ] Portfolio analytics executed using real-time JSON input (`--json-input workspace/live_holdings.json`).
- [ ] Valid `order_id` or `trigger_id` generated for trade executions.

---

## References
- [references/gtt-order-specs.md](references/gtt-order-specs.md) — GTT trigger types, tick size rules, slippage buffers, and validation rules.
