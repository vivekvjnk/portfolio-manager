#!/usr/bin/env python3
"""
Portfolio Calculator & Sector Concentration Analytics Tool
Provides deterministic calculations for portfolio valuation, daily returns,
sector weight distribution, and underperformer identification.
"""

import sys
import json
import argparse

# Default sector map for known portfolio holdings
SECTOR_MAP = {
    "ADANIPOWER": {"sector": "Power", "is_psu": False},
    "BEL": {"sector": "Defence", "is_psu": True},
    "BEML": {"sector": "Defence/Capital Goods", "is_psu": True},
    "BHEL": {"sector": "Power/Capital Goods", "is_psu": True},
    "COCHINSHIP": {"sector": "Defence/Shipbuilding", "is_psu": True},
    "ETERNAL": {"sector": "Consumer", "is_psu": False},
    "HAL": {"sector": "Defence/Aerospace", "is_psu": True},
    "ICICIBANK": {"sector": "Financials", "is_psu": False},
    "IOC": {"sector": "Oil & Gas", "is_psu": True},
    "JSWENERGY": {"sector": "Power", "is_psu": False},
    "MAZDOCK": {"sector": "Defence/Shipbuilding", "is_psu": True},
    "NAZARA": {"sector": "Gaming/Tech", "is_psu": False},
    "NTPC": {"sector": "Power", "is_psu": True},
    "NTPCGREEN": {"sector": "Power/Renewables", "is_psu": True},
    "POWERGRID": {"sector": "Power", "is_psu": True},
    "RPOWER": {"sector": "Power", "is_psu": False},
    "RVNL": {"sector": "Railway/Infra", "is_psu": True},
    "SBIN": {"sector": "Financials", "is_psu": True},
    "SUZLON": {"sector": "Power/Renewables", "is_psu": False},
    "TATAPOWER": {"sector": "Power", "is_psu": False},
    "TORNTPOWER": {"sector": "Power", "is_psu": False},
    "TRENT": {"sector": "Retail", "is_psu": False},
}

DEFAULT_HOLDINGS = [
    {"tradingsymbol":"ADANIPOWER","quantity":144,"last_price":202.98,"close_price":200.83,"day_change":2.15},
    {"tradingsymbol":"BEL","quantity":73,"last_price":451.55,"close_price":457.65,"day_change":-6.10},
    {"tradingsymbol":"BEML","quantity":2,"last_price":1768.9,"close_price":1744.5,"day_change":24.40},
    {"tradingsymbol":"BHEL","quantity":40,"last_price":332.61,"close_price":325.63,"day_change":6.98},
    {"tradingsymbol":"COCHINSHIP","quantity":88,"last_price":1556.9,"close_price":1544.9,"day_change":12.00},
    {"tradingsymbol":"ETERNAL","quantity":100,"last_price":259.48,"close_price":254.88,"day_change":4.60},
    {"tradingsymbol":"HAL","quantity":5,"last_price":4358.4,"close_price":4344.5,"day_change":13.90},
    {"tradingsymbol":"ICICIBANK","quantity":42,"last_price":1388.4,"close_price":1356.2,"day_change":32.20},
    {"tradingsymbol":"IOC","quantity":200,"last_price":147.4,"close_price":147.0,"day_change":0.40},
    {"tradingsymbol":"JSWENERGY","quantity":70,"last_price":546.65,"close_price":543.05,"day_change":3.60},
    {"tradingsymbol":"MAZDOCK","quantity":13,"last_price":2656.6,"close_price":2621.2,"day_change":35.40},
    {"tradingsymbol":"NAZARA","quantity":220,"last_price":275.75,"close_price":270.08,"day_change":5.67},
    {"tradingsymbol":"NTPC","quantity":437,"last_price":396.2,"close_price":398.0,"day_change":-1.80},
    {"tradingsymbol":"NTPCGREEN","quantity":355,"last_price":111.69,"close_price":113.0,"day_change":-1.31},
    {"tradingsymbol":"POWERGRID","quantity":251,"last_price":319.35,"close_price":319.7,"day_change":-0.35},
    {"tradingsymbol":"RPOWER","quantity":71,"last_price":28.36,"close_price":28.09,"day_change":0.27},
    {"tradingsymbol":"RVNL","quantity":112,"last_price":298.86,"close_price":296.33,"day_change":2.53},
    {"tradingsymbol":"SBIN","quantity":23,"last_price":1111.85,"close_price":1107.85,"day_change":4.00},
    {"tradingsymbol":"SUZLON","quantity":1005,"last_price":53.1,"close_price":52.5,"day_change":0.60},
    {"tradingsymbol":"TATAPOWER","quantity":228,"last_price":435.7,"close_price":433.65,"day_change":2.05},
    {"tradingsymbol":"TORNTPOWER","quantity":22,"last_price":1621.5,"close_price":1606.3,"day_change":15.20},
    {"tradingsymbol":"TRENT","quantity":6,"last_price":4393.45,"close_price":4242.85,"day_change":150.60}
]

def analyze_portfolio(holdings, nifty_return=0.87):
    total_curr_val = 0.0
    total_prev_val = 0.0
    total_day_change = 0.0

    sector_totals = {}
    psu_value = 0.0
    holding_details = []

    for h in holdings:
        symbol = h["tradingsymbol"]
        qty = float(h["quantity"])
        last_price = float(h["last_price"])
        close_price = float(h.get("close_price", last_price - h.get("day_change", 0.0)))
        day_change = float(h.get("day_change", last_price - close_price))

        curr_val = qty * last_price
        prev_val = qty * close_price
        abs_change = qty * day_change
        pct_change = (day_change / close_price * 100) if close_price else 0.0

        total_curr_val += curr_val
        total_prev_val += prev_val
        total_day_change += abs_change

        sec_info = SECTOR_MAP.get(symbol, {"sector": "Other", "is_psu": False})
        primary_sector = sec_info["sector"].split("/")[0]

        sector_totals[primary_sector] = sector_totals.get(primary_sector, 0.0) + curr_val
        if sec_info.get("is_psu", False):
            psu_value += curr_val

        holding_details.append({
            "symbol": symbol,
            "quantity": qty,
            "last_price": last_price,
            "close_price": close_price,
            "current_value": curr_val,
            "day_change_abs": abs_change,
            "day_change_pct": pct_change,
            "sector": sec_info["sector"],
            "is_psu": sec_info["is_psu"]
        })

    portfolio_return = (total_day_change / total_prev_val * 100) if total_prev_val else 0.0

    # Sector Breakdown %
    sector_weights = {}
    for sec, val in sector_totals.items():
        sector_weights[sec] = round((val / total_curr_val * 100), 2) if total_curr_val else 0.0

    psu_pct = round((psu_value / total_curr_val * 100), 2) if total_curr_val else 0.0

    # Sort holdings by day change %
    holding_details.sort(key=lambda x: x["day_change_pct"], reverse=True)

    return {
        "summary": {
            "total_current_value": round(total_curr_val, 2),
            "total_previous_value": round(total_prev_val, 2),
            "total_day_change": round(total_day_change, 2),
            "portfolio_return_pct": round(portfolio_return, 2),
            "nifty_return_pct": nifty_return,
            "outperforming_nifty": portfolio_return > nifty_return,
            "psu_concentration_pct": psu_pct,
        },
        "sector_weights_pct": sector_weights,
        "top_gainers": holding_details[:3],
        "top_losers": holding_details[-3:][::-1],
        "holdings": holding_details
    }

def main():
    parser = argparse.ArgumentParser(description="Portfolio Analytics & Sector Breakdown")
    parser.add_argument("--json-input", help="Path to JSON file containing holdings")
    parser.add_argument("--nifty-return", type=float, default=0.87, help="Nifty 50 return percentage for benchmark comparison")
    parser.add_argument("--output-json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    holdings = DEFAULT_HOLDINGS
    if args.json_input:
        with open(args.json_input, "r") as f:
            holdings = json.load(f)

    res = analyze_portfolio(holdings, nifty_return=args.nifty_return)

    if args.output_json:
        print(json.dumps(res, indent=2))
        return

    s = res["summary"]
    print("=" * 60)
    print("PORTFOLIO ANALYTICS REPORT")
    print("=" * 60)
    print(f"Total Current Value:  ₹{s['total_current_value']:,.2f}")
    print(f"Total Daily Change:   ₹{s['total_day_change']:,.2f}")
    print(f"Portfolio Return:     {s['portfolio_return_pct']:.2f}%")
    print(f"Nifty 50 Return:      {s['nifty_return_pct']:.2f}%")
    print(f"Benchmark Status:     {'OUTPERFORMING' if s['outperforming_nifty'] else 'UNDERPERFORMING'}")
    print(f"PSU Exposure:         {s['psu_concentration_pct']:.2f}%")
    print("-" * 60)
    print("SECTOR WEIGHT DISTRIBUTION:")
    for sec, weight in sorted(res["sector_weights_pct"].items(), key=lambda x: x[1], reverse=True):
        alert = " [WARNING: HEAVY CONCENTRATION]" if weight > 30 else ""
        print(f"  - {sec:<22}: {weight:5.2f}%{alert}")
    print("-" * 60)
    print("TOP GAINERS (DAY):")
    for g in res["top_gainers"]:
        print(f"  + {g['symbol']:<12}: {g['day_change_pct']:+6.2f}% (+₹{g['day_change_abs']:,.2f})")
    print("TOP LOSERS (DAY):")
    for l in res["top_losers"]:
        print(f"  - {l['symbol']:<12}: {l['day_change_pct']:+6.2f}% (₹{l['day_change_abs']:,.2f})")
    print("=" * 60)

if __name__ == "__main__":
    main()
