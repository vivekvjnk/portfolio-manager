# Stock selection guide
## 1. Market Universe & Data Integrity

* Universe:

  * NIFTY 50, NIFTY 100 stocks (cash segment only)

* Filters:

  * Price > ₹100
  * Average Volume > 1,000,000
  * Exclude stocks with circuit hits in last 10 days
  * Exclude stocks within 5 trading days of earnings

* Preprocess:

  * Adjust for splits/dividends
  * Clean missing or abnormal values

Trade ONLY when:

* Stock of interest is above both 20 EMA and 50 EMA
* ADX > 25

DO NOT TRADE when:

* Stock of interest is between EMAs
* ADX < 20

---

## 2. TIMEFRAME

* Daily timeframe only
* No lower timeframe noise
