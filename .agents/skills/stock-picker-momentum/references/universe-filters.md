# Stock Universe & Momentum Selection Guidelines

## 1. Approved Universe & Liquidity Hard Rules
To protect retail capital from illiquid traps and manipulation:

- **Approved Universe**: Cash segment stocks belonging to **NIFTY 50** or **NIFTY 100** indices only.
- **Minimum Share Price**: Price > **₹100**.
- **Minimum Average Volume**: 20-day Average Daily Volume > **1,000,000 shares**.
- **Segment Filter**: Cash segment only (No illiquid derivatives or penny stocks).

---

## 2. Hard Exclusion Criteria
Do **NOT** select or trade any stock meeting any of these conditions:

1. **Pre-Earnings Window**: Stock has scheduled earnings/results announcement within **5 trading days**.
2. **Circuit Hit History**: Stock has hit upper or lower price circuit in the last **10 trading days**.
3. **EMA Compression / Squeeze**: Price trading between 20 EMA and 50 EMA.
4. **Weak ADX**: ADX(14) < **20**.

---

## 3. Momentum & Structure Criteria
Selections must exhibit strong structure-based momentum:

- **Higher High / Higher Low Structure**: Confirmed higher high progression using 3-candle pivot logic.
- **Trend Strength**: Price trading above both **20 EMA** and **50 EMA**.
- **Demand Zone Retracement**: Price pulling back into a valid demand zone (width $\le 1.5 \times \text{ATR}$) following a valid BOS breakout.
- **Volume Confirmation**: Pullback volume drying up; entry candle volume above average.

---

## 4. Trade Risk Management & Targets

| Parameter | Standard Rule | Example |
|---|---|---|
| **Stop Loss (SL)** | Demand Zone Low minus **0.3% buffer** | Demand Zone Low = ₹400 → SL = ₹398.80 |
| **Initial Risk ($R$)** | $\text{Entry Price} - \text{SL Price}$ | Entry = ₹420, SL = ₹398.80 → $R = \text{₹}21.20$ |
| **Partial Target (1:1)** | Entry Price $+ 1.0 \times R$ | Target 1 = ₹441.20 (Exit 50% position, move SL to breakeven) |
| **Final Target (1:2)** | Entry Price $+ 2.0 \times R$ | Target 2 = ₹462.40 (Exit remaining 50% or trail with 20 EMA) |
