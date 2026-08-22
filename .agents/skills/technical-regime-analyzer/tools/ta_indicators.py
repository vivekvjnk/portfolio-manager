#!/usr/bin/env python3
"""
Technical Analysis & Structure Indicators Calculator
Provides deterministic calculations for:
- 20 EMA & 50 EMA
- ADX (Average Directional Index - 14 period)
- ATR (Average True Range - 14 period)
- 3-candle pivot detection (Swing Highs / Swing Lows)
- Break of Structure (BOS) breakout candle validation (Body %, Range vs ATR, Volume multiplier)
"""

import sys
import json
import math
import argparse

def calculate_ema(prices, period):
    if len(prices) < period:
        return [None] * len(prices)
    multiplier = 2 / (period + 1)
    ema = [sum(prices[:period]) / period]
    for p in prices[period:]:
        ema.append((p - ema[-1]) * multiplier + ema[-1])
    return [None] * (period - 1) + ema

def calculate_atr(highs, lows, closes, period=14):
    if len(closes) <= period:
        return [None] * len(closes)
    tr = [highs[0] - lows[0]]
    for i in range(1, len(closes)):
        tr1 = highs[i] - lows[i]
        tr2 = abs(highs[i] - closes[i-1])
        tr3 = abs(lows[i] - closes[i-1])
        tr.append(max(tr1, tr2, tr3))
    
    atr = [sum(tr[:period]) / period]
    for i in range(period, len(tr)):
        atr.append((atr[-1] * (period - 1) + tr[i]) / period)
    return [None] * (period - 1) + atr

def calculate_adx(highs, lows, closes, period=14):
    if len(closes) < period * 2:
        return [None] * len(closes)
    
    tr, pos_dm, neg_dm = [], [], []
    for i in range(1, len(closes)):
        up_move = highs[i] - highs[i-1]
        down_move = lows[i-1] - lows[i]
        
        pos_dm.append(up_move if (up_move > down_move and up_move > 0) else 0)
        neg_dm.append(down_move if (down_move > up_move and down_move > 0) else 0)
        
        tr1 = highs[i] - lows[i]
        tr2 = abs(highs[i] - closes[i-1])
        tr3 = abs(lows[i] - closes[i-1])
        tr.append(max(tr1, tr2, tr3))
        
    smooth_tr = [sum(tr[:period])]
    smooth_pos_dm = [sum(pos_dm[:period])]
    smooth_neg_dm = [sum(neg_dm[:period])]
    
    for i in range(period, len(tr)):
        smooth_tr.append(smooth_tr[-1] - (smooth_tr[-1] / period) + tr[i])
        smooth_pos_dm.append(smooth_pos_dm[-1] - (smooth_pos_dm[-1] / period) + pos_dm[i])
        smooth_neg_dm.append(smooth_neg_dm[-1] - (smooth_neg_dm[-1] / period) + neg_dm[i])
        
    pos_di = [(p / t * 100) if t else 0 for p, t in zip(smooth_pos_dm, smooth_tr)]
    neg_di = [(n / t * 100) if t else 0 for n, t in zip(smooth_neg_dm, smooth_tr)]
    
    dx = []
    for p, n in zip(pos_di, neg_di):
        diff = abs(p - n)
        sum_di = p + n
        dx.append((diff / sum_di * 100) if sum_di else 0)
        
    if len(dx) < period:
        return [None] * len(closes)
        
    adx = [sum(dx[:period]) / period]
    for i in range(period, len(dx)):
        adx.append((adx[-1] * (period - 1) + dx[i]) / period)
        
    padding = len(closes) - len(adx)
    return [None] * padding + adx

def detect_3candle_pivots(highs, lows):
    """
    3-candle pivot method:
    Swing High: High[t-1] > High[t-2] and High[t-1] > High[t]
    Swing Low:  Low[t-1] < Low[t-2] and Low[t-1] < Low[t]
    """
    swing_highs = []
    swing_lows = []
    
    for i in range(2, len(highs)):
        if highs[i-1] > highs[i-2] and highs[i-1] > highs[i]:
            swing_highs.append({"index": i-1, "price": highs[i-1]})
        if lows[i-1] < lows[i-2] and lows[i-1] < lows[i]:
            swing_lows.append({"index": i-1, "price": lows[i-1]})
            
    return swing_highs, swing_lows

def evaluate_bos_candle(open_p, high_p, low_p, close_p, volume, avg_volume, atr_val):
    candle_range = high_p - low_p
    body_length = abs(close_p - open_p)
    
    body_ratio = (body_length / candle_range) if candle_range else 0.0
    range_atr_ratio = (candle_range / atr_val) if atr_val else 0.0
    vol_multiplier = (volume / avg_volume) if avg_volume else 0.0
    
    is_valid_bos = (
        body_ratio >= 0.60 and
        range_atr_ratio >= 1.0 and
        vol_multiplier >= 1.5
    )
    
    return {
        "is_valid_bos": is_valid_bos,
        "body_ratio_pct": round(body_ratio * 100, 2),
        "range_atr_ratio": round(range_atr_ratio, 2),
        "volume_multiplier": round(vol_multiplier, 2),
        "checks": {
            "body_ge_60pct": body_ratio >= 0.60,
            "range_ge_1atr": range_atr_ratio >= 1.0,
            "volume_ge_1_5x": vol_multiplier >= 1.5
        }
    }

def analyze_ohlcv(candles, symbol="STOCK"):
    opens = [c["open"] for c in candles]
    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]
    closes = [c["close"] for c in candles]
    volumes = [c["volume"] for c in candles]
    
    ema20 = calculate_ema(closes, 20)
    ema50 = calculate_ema(closes, 50)
    adx14 = calculate_adx(highs, lows, closes, 14)
    atr14 = calculate_atr(highs, lows, closes, 14)
    
    swing_highs, swing_lows = detect_3candle_pivots(highs, lows)
    
    last_close = closes[-1]
    last_ema20 = ema20[-1]
    last_ema50 = ema50[-1]
    last_adx = adx14[-1]
    last_atr = atr14[-1]
    
    # Regime determination
    regime = "SIDEWAYS"
    if last_ema20 and last_ema50 and last_adx:
        if last_close > last_ema20 and last_close > last_ema50 and last_adx > 25:
            regime = "TRENDING_UP"
        elif last_close < last_ema20 and last_close < last_ema50 and last_adx > 25:
            regime = "TRENDING_DOWN"
            
    # Check BOS on last candle if swing high exists
    bos_eval = None
    if swing_highs and last_atr:
        recent_sh = swing_highs[-1]["price"]
        if last_close > recent_sh:
            avg_vol = sum(volumes[-20:-1]) / 20 if len(volumes) >= 21 else sum(volumes) / len(volumes)
            bos_eval = evaluate_bos_candle(
                opens[-1], highs[-1], lows[-1], closes[-1], volumes[-1], avg_vol, last_atr
            )
            
    return {
        "symbol": symbol,
        "last_price": last_close,
        "ema20": round(last_ema20, 2) if last_ema20 else None,
        "ema50": round(last_ema50, 2) if last_ema50 else None,
        "adx14": round(last_adx, 2) if last_adx else None,
        "atr14": round(last_atr, 2) if last_atr else None,
        "regime": regime,
        "recent_swing_high": swing_highs[-1] if swing_highs else None,
        "recent_swing_low": swing_lows[-1] if swing_lows else None,
        "bos_evaluation": bos_eval
    }

def main():
    parser = argparse.ArgumentParser(description="Technical Indicators & BOS Structure Calculator")
    parser.add_argument("--json-input", help="Path to JSON file containing daily OHLCV candles")
    parser.add_argument("--symbol", default="NIFTY50", help="Trading symbol")
    parser.add_argument("--output-json", action="store_true", help="Output JSON results")
    args = parser.parse_args()
    
    if not args.json_input:
        print("Usage: ta_indicators.py --json-input <path_to_ohlcv_json> [--symbol SYMBOL] [--output-json]")
        sys.exit(1)
        
    with open(args.json_input, "r") as f:
        candles = json.load(f)
        
    res = analyze_ohlcv(candles, symbol=args.symbol)
    if args.output_json:
        print(json.dumps(res, indent=2))
    else:
        print("=" * 60)
        print(f"TECHNICAL STRUCTURE ANALYSIS: {res['symbol']}")
        print("=" * 60)
        print(f"Last Price:  ₹{res['last_price']:,.2f}")
        print(f"20 EMA:      ₹{res['ema20']}")
        print(f"50 EMA:      ₹{res['ema50']}")
        print(f"ADX(14):     {res['adx14']}")
        print(f"ATR(14):     ₹{res['atr14']}")
        print(f"REGIME:      {res['regime']}")
        if res['recent_swing_high']:
            print(f"Swing High:  ₹{res['recent_swing_high']['price']:,.2f}")
        if res['bos_evaluation']:
            bos = res['bos_evaluation']
            print("-" * 60)
            print(f"BOS BREAKOUT DETECTED: Valid={bos['is_valid_bos']}")
            print(f"  - Body Ratio: {bos['body_ratio_pct']}% (Req >= 60%)")
            print(f"  - Range/ATR:  {bos['range_atr_ratio']}x (Req >= 1.0x)")
            print(f"  - Vol Mult:   {bos['volume_multiplier']}x (Req >= 1.5x)")
        print("=" * 60)

if __name__ == "__main__":
    main()
