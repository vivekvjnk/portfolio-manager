# Market Regime Engine & Stock Regime Scoring Specifications

## 1. Market Level Regime Classification (NIFTY 50)
Applied on the **Daily Timeframe**:

| Market State | Nifty Technical Criteria | Action Rule |
|---|---|---|
| **Trending Up** | Nifty > 20 EMA **AND** > 50 EMA; **ADX(14) > 25**; Weekly > 20 EMA | **LONG trades permitted.** Active deployment allowed. |
| **Trending Down** | Nifty < 20 EMA **AND** < 50 EMA; **ADX(14) > 25** | **HARD RULE: NO LONG TRADES PERMITTED.** Protect capital; sit in cash. |
| **Sideways** | Nifty between 20 & 50 EMA **OR** **ADX(14) < 20** | **DEFENSIVE MODE.** Reduce position sizing by 50%; trade only top 5% RS setups. |

---

## 2. Stock-Level Quantified Regime Score
For individual stock setup evaluation, compute the **Regime Score (0.0 to 1.0)**:

$$\text{Regime Score} = \frac{S_{\text{market}} + S_{\text{adx}} + S_{\text{ema}} + S_{\text{sector}}}{4}$$

| Component | Score = 1.0 | Score = 0.5 | Score = 0.0 |
|---|---|---|---|
| **$S_{\text{market}}$ (Market Alignment)** | Nifty Trending Up | Nifty Sideways | Nifty Trending Down |
| **$S_{\text{adx}}$ (Stock ADX Strength)** | ADX ≥ 30 | 20 ≤ ADX < 30 | ADX < 20 |
| **$S_{\text{ema}}$ (EMA Alignment)** | Price > 20 EMA & 20 EMA > 50 EMA | Price > 50 EMA but < 20 EMA | Price < 20 EMA & < 50 EMA |
| **$S_{\text{sector}}$ (Sector Relative Strength)** | Sector Outperforming Nifty (20D) | Sector In-line with Nifty | Sector Underperforming Nifty |

### Execution Threshold
- **Regime Score ≥ 0.60**: Valid setup eligible for trade entry approval.
- **Regime Score < 0.60**: REJECT SETUP. Do not enter.

---

## 3. Structure-Based Mechanics (3-Candle Pivot & BOS)

### A. 3-Candle Swing Pivot Rules
- **Swing High**: Candle $t-1$ where $\text{High}_{t-1} > \text{High}_{t-2}$ and $\text{High}_{t-1} > \text{High}_{t}$.
- **Swing Low**: Candle $t-1$ where $\text{Low}_{t-1} < \text{Low}_{t-2}$ and $\text{Low}_{t-1} < \text{Low}_{t}$.

### B. Break of Structure (BOS) Validation Checklist
To confirm a valid institutional BOS breakout:
1. **Closing Price**: Daily Close > confirmed swing high price.
2. **Candle Body**: $\frac{\text{Body}}{\text{High} - \text{Low}} \ge 60\%$.
3. **Range**: $(\text{High} - \text{Low}) \ge 1.0 \times \text{ATR}(14)$.
4. **Volume**: $\text{Volume} \ge 1.5 \times \text{Average Volume}(20)$.

---

## 4. Demand Zone & Retracement Rules
- **Zone Definition**: The last bearish candle prior to the BOS breakout candle.
- **Zone Width Constraint**: Zone Width ($\text{High}_{\text{zone}} - \text{Low}_{\text{zone}}) \le 1.5 \times \text{ATR}(14)$.
- **Retracement Criteria**: Price must retrace into the demand zone without closing strongly below $\text{Low}_{\text{zone}}$.
- **Entry Trigger**: Formation of a bullish confirmation candle closing above the prior candle's high with Body $\ge 60\%$.
