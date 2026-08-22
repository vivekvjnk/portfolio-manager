# Zerodha GTT (Good Till Triggered) Order Specifications

## 1. Overview of GTT Orders
GTT orders allow automated, long-term trigger-based order placement in Indian equity markets without requiring daily order re-entry. They remain active until triggered or cancelled (up to 1 year).

---

## 2. Trigger Types & Specifications

### A. Single Trigger (Stop Loss OR Target)
Used primarily for downside stop-loss protection or breakout buy triggers.

| Parameter | Specification | Rule / Precision |
|---|---|---|
| **Trigger Price** | Price at which the limit order is released to the exchange. | Must be rounded to nearest ₹0.05 tick size. |
| **Limit Price** | Execution price sent to order book once triggered. | For SELL SL: Set **0.1% – 0.2% below** Trigger Price to ensure fill during fast moves. |
| **Quantity** | Number of shares to execute. | Exact integer string with Decimal rounding. |

### B. One-Cancels-the-Other (OCO) Trigger (Stop Loss AND Target)
Used for simultaneous stop-loss protection and profit-booking targets on existing holdings.

- **Condition 1 (Stop Loss)**: Trigger Price ≤ Stop Loss level.
- **Condition 2 (Target)**: Trigger Price ≥ Profit Target level.
- **Execution**: When either condition triggers, the corresponding order is placed and the other condition is automatically cancelled.

---

## 3. Decimal Precision & Tick Size Formatting
To avoid float rounding errors and exchange rejection (`Invalid Price Tick`):

$$\text{Valid Price} = \text{Round}\left(\text{Price}, \text{tick}=0.05\right)$$

- Always format price parameters as 2-decimal strings (e.g. `"409.50"`, NOT `409.49999999999994`).
- Always format quantity parameters as exact integers (e.g. `50`, NOT `50.0`).

---

## 4. Pre-Execution Validation Checklist
Before calling `place-gtt` or `place-order`:
1. **Holding Verification**: Confirm current holdings count via `kite_cli.py holdings`.
2. **Slippage Buffer**: Confirm limit price buffer ($\text{Limit Price} \le \text{Trigger Price} - 0.10$ for Sell SL).
3. **Capital Reserve Check**: Confirm order does not violate minimum 15% War Chest cash requirement.
4. **Concentration Check**: Confirm position sizing does not push total sector weight above 30%.
