class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.prices = []

    def set_price(self, prices):
        self.prices = prices

    def current_price(self):
        return self.prices[-1]
    
    def high(self):
        return max(self.prices)
    
    def is_breakout(self):
        if self.current_price() >= self.high():
            return True
        else:
            return False
        

import csv 
import os 

class Data_fetcher:
    def __init__(self,datafolder):
        self.datafolder = datafolder

    #since we already have data folder name we will construct the path and if it exists we will open the symbol.csv with dictread and read its close values and convert them in float and append the price = [] that we will create 

    def fetch_full_data(self, symbol):
        """Fetch Close prices from the CSV."""
        data = {"Close": []}
        filepath = os.path.join(self.datafolder, f"{symbol}.csv")

        if not os.path.exists(filepath):
            return data

        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            header = next(reader, [])
            next(reader, None)
            next(reader, None)

            try:
                close_idx = header.index("Close")
            except ValueError:
                close_idx = 1

            for row in reader:
                if not row: continue
                try:
                    data["Close"].append(float(row[close_idx]))
                except (ValueError, IndexError):
                    continue
        return data

    def fetch_price(self, symbol):
        """Backwards compatibility for fetching just prices."""
        data = self.fetch_full_data(symbol)
        return data.get("Close", [])

def download_data(symbols, datafolder, time_frame=1, on_progress=None):
    """Download stock data from Yahoo Finance.
    
    Args:
        symbols: List of stock symbols to download.
        datafolder: Path to save CSV files.
        time_frame: Number of years of historical data (default 1).
        on_progress: Optional callback(symbol, current_index, total) for progress updates.
    """
    import yfinance as yf
    os.makedirs(datafolder, exist_ok=True)
    total = len(symbols)

    for i, symbol in enumerate(symbols):
        if on_progress:
            on_progress(symbol, i, total)
        data = yf.download(symbol, period=f"{time_frame}y", progress=False)
        file_path = os.path.join(datafolder, f"{symbol}.csv")
        data.to_csv(file_path)

    return total


TRADING_DAYS_PER_YEAR = 252

def _period_metrics(prices, current, period_label):
    """Compute high/low/avg/breakout metrics for a price slice."""
    if not prices:
        return {}
    high = max(prices)
    low = min(prices)
    avg = sum(prices) / len(prices)
    pct_from_high = round((current / high - 1) * 100, 2) if high > 0 else 0
    return {
        f"{period_label} High": round(high, 2),
        f"{period_label} Low": round(low, 2),
        f"{period_label} Avg": round(avg, 2),
        f"% From {period_label} High": pct_from_high,
        f"{period_label} Breakout": current >= high,
        f"{period_label} Breakdown": current <= low if low > 0 else False,
        f"Near {period_label} High": current >= high * 0.95,
        f"Near {period_label} Low": current <= low * 1.05 if low > 0 else False,
        f"Above {period_label} Avg": current > avg,
    }

def _calc_return(prices, days):
    """Calculate % return over last N trading days."""
    if len(prices) < days + 1:
        return None
    old = prices[-(days + 1)]
    new = prices[-1]
    return ((new - old) / old) * 100 if old > 0 else None

def _load_nifty_prices(data_dir):
    """Load Nifty 50 (^NSEI) prices from the data folder."""
    fetcher = Data_fetcher(data_dir)
    return fetcher.fetch_price("^NSEI")

def run_screener(symbols, data_dir):
    """Run screener computing metrics for 1Y, 2Y, 5Y, All Time, and RS."""
    fetcher = Data_fetcher(data_dir)
    results = []

    # Load Nifty 50 benchmark once
    nifty_prices = _load_nifty_prices(data_dir)
    nifty_ret_275 = _calc_return(nifty_prices, 275) if len(nifty_prices) > 275 else None
    nifty_ret_123 = _calc_return(nifty_prices, 123) if len(nifty_prices) > 123 else None

    for symbol in symbols:
        # stock = Stock(symbol)  # We can still use Stock class if needed for methods
        full_data = fetcher.fetch_full_data(symbol)
        prices = full_data["Close"]

        if len(prices) == 0:
            continue
        
        current = prices[-1]

        row = {
            "Symbol": symbol.replace(".NS", ""),
            "Full Symbol": symbol,
            "Current Price": round(current, 2),
        }

        # --- Period slices (Price) ---
        periods = {
            "1Y": prices[-TRADING_DAYS_PER_YEAR:],
            "2Y": prices[-TRADING_DAYS_PER_YEAR * 2:],
            "5Y": prices[-TRADING_DAYS_PER_YEAR * 5:],
            "AT": prices,
        }

        for label, slice_prices in periods.items():
            row.update(_period_metrics(slice_prices, current, label))

        # --- Relative Strength vs Nifty 50 ---
        stock_ret_275 = _calc_return(prices, 275)
        stock_ret_123 = _calc_return(prices, 123)

        row["Stock Ret 55W"] = round(stock_ret_275, 2) if stock_ret_275 is not None else None
        row["Stock Ret 123D"] = round(stock_ret_123, 2) if stock_ret_123 is not None else None
        row["Nifty Ret 55W"] = round(nifty_ret_275, 2) if nifty_ret_275 is not None else None
        row["Nifty Ret 123D"] = round(nifty_ret_123, 2) if nifty_ret_123 is not None else None

        row["RS 55W Outperformer"] = (
            stock_ret_275 is not None and nifty_ret_275 is not None and stock_ret_275 > nifty_ret_275
        )
        row["RS 123D Outperformer"] = (
            stock_ret_123 is not None and nifty_ret_123 is not None and stock_ret_123 > nifty_ret_123
        )
        row["RS 55W Underperformer"] = (
            stock_ret_275 is not None and nifty_ret_275 is not None and stock_ret_275 < nifty_ret_275
        )
        row["RS 123D Underperformer"] = (
            stock_ret_123 is not None and nifty_ret_123 is not None and stock_ret_123 < nifty_ret_123
        )

        results.append(row)

    return results




#----------------------------MAIN------------------------------

if __name__ == "__main__":

    # ---- selecting the time frame and sector ----

    mode = int(input("enter the time frame:"))
    sector = input("enter the sector")

    # ---- getting required data ---- 

    symbols = []

    with open(os.path.join('NAMES', f'{sector}.csv'), 'r') as file:
        reader = csv.reader(file)

        for row in reader :
            symbols.append(row[0])

    #check if "data" folder exists 

    datafolder = 'data'

    if not os.path.exists(datafolder):
        print("Created 'data' folder")

        def print_progress(symbol, i, total):
            print(f"Downloading {symbol}... ({i+1}/{total})")

        count = download_data(symbols, datafolder, time_frame=mode, on_progress=print_progress)
        print(f"All {count} downloads complete!")
    else :
        print("Data folder already exists. skipping downloads")

    # --- Run the master engine and filter for All-Time Breakouts ---
    all_results = run_screener(symbols, datafolder)
    result = []
    for r in all_results:
        if r.get("AT Breakout") == True:
            result.append(r["Full Symbol"])


    with open("screener_output.csv", mode="w", newline="") as file:

        writer = csv.writer(file)
        writer.writerow(["Symbol"])

        for symbol in result:
            writer.writerow([symbol])

    print("Items filtered and Listed in screener_output.csv")
