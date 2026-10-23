# CandleScope - Trading Bot
# Built on Pydroid3 | Arusha TZ | Qson48
# Live Binance API + Chart + Monthly Report + Risk Management

import os
import time
import datetime
import pandas as pd
from binance.client import Client
import matplotlib.pyplot as plt

# === CONFIG ===
API_KEY = os.getenv("BINANCE_API_KEY")  # Weka kwenye .env, usiweke hapa!
API_SECRET = os.getenv("BINANCE_SECRET")

SYMBOL = "BTCUSDT"
INTERVAL = Client.KLINE_INTERVAL_1HOUR
RISK_PER_TRADE = 0.02  # 2% risk
STOP_LOSS_PCT = 0.015  # 1.5%

client = Client(API_KEY, API_SECRET, testnet=True)  # Tumia testnet kwanza

def get_candles(symbol=SYMBOL, interval=INTERVAL, limit=100):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'open_time','open','high','low','close','volume',
        'close_time','qav','trades','tb_base','tb_quote','ignore'
    ])
    df[['open','high','low','close']] = df[['open','high','low','close']].astype(float)
    return df

def calculate_risk(balance, entry_price):
    """Risk Management - 2% per trade"""
    risk_amount = balance * RISK_PER_TRADE
    qty = risk_amount / (entry_price * STOP_LOSS_PCT)
    return round(qty, 5)

def generate_chart(df):
    """Chart for monthly report"""
    plt.figure(figsize=(10,4))
    plt.plot(df['close'], label='Close Price')
    plt.title(f'{SYMBOL} - CandleScope Chart')
    plt.legend()
    plt.savefig('chart.png')
    print("[CandleScope] Chart saved: chart.png")

def monthly_report(df):
    """Monthly Report"""
    month = datetime.datetime.now().strftime("%Y-%m")
    start = df['close'].iloc[0]
    end = df['close'].iloc[-1]
    change = ((end - start) / start) * 100
    
    report = f"""
=== CandleScope Monthly Report - {month} ===
Symbol: {SYMBOL}
Start Price: {start}
End Price: {end}
Change: {change:.2f}%
Total Candles Analyzed: {len(df)}
Status: Active
Built on: Pydroid3 Mobile - Arusha
"""
    with open(f"report_{month}.txt", "w") as f:
        f.write(report)
    print(report)

def run():
    print("🕯️ CandleScope Bot Started...")
    balance = 1000  # Demo balance - testnet
    
    while True:
        try:
            df = get_candles()
            current_price = df['close'].iloc[-1]
            qty = calculate_risk(balance, current_price)
            
            print(f"[{datetime.datetime.now()}] {SYMBOL}: {current_price} | Qty: {qty} | Risk: {RISK_PER_TRADE*100}%")
            
            # Hapa unaweka logic yako ya kuingia sokoni
            # if buy_signal: client.create_order(...)
            
            # Kila saa 24 generate report
            # monthly_report(df)
            
            time.sleep(3600)  # Angalia kila saa
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run()
