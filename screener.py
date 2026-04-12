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

    def fetch_price(self, symbol):
        """Backwards compatibility for fetching just prices."""
        data = self.fetch_full_data(symbol)
        return data.get("Close", [])

    def fetch_full_data(self, symbol):
        """Fetch Close prices, Volume, DeliveryVolume, and DeliveryPercentage."""
        data = {"Close": [], "Volume": [], "DeliveryVolume": [], "DeliveryPercentage": []}
        filepath = os.path.join(self.datafolder, f"{symbol}.csv")

        if not os.path.exists(filepath):
            return data

        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            header1 = next(reader, [])
            header2 = next(reader, [])
            header3 = next(reader, [])

            try:
                close_idx = header1.index("Close")
                vol_idx = header1.index("Volume") if "Volume" in header1 else -1
                dvol_idx = header1.index("DeliveryVolume") if "DeliveryVolume" in header1 else -1
                dpct_idx = header1.index("DeliveryPercentage") if "DeliveryPercentage" in header1 else -1
            except ValueError:
                close_idx, vol_idx, dvol_idx, dpct_idx = 1, 5, -1, -1

            for row in reader:
                if not row: continue
                try:
                    data["Close"].append(float(row[close_idx]))
                    
                    # Total Traded Volume
                    if vol_idx != -1 and len(row) > vol_idx:
                        v = row[vol_idx].replace(",", "").strip()
                        data["Volume"].append(float(v) if v else 0.0)
                    else:
                        data["Volume"].append(0.0)

                    # Delivery Volume
                    if dvol_idx != -1 and len(row) > dvol_idx and row[dvol_idx].strip():
                        val = row[dvol_idx].replace(",", "").strip()
                        data["DeliveryVolume"].append(float(val) if val and val != "-" else 0.0)
                    else:
                        data["DeliveryVolume"].append(0.0)

                    # Delivery Percentage
                    if dpct_idx != -1 and len(row) > dpct_idx and row[dpct_idx].strip():
                        val = row[dpct_idx].replace(",", "").strip()
                        data["DeliveryPercentage"].append(float(val) if val and val != "-" else 0.0)
                    else:
                        data["DeliveryPercentage"].append(0.0)
                except (ValueError, IndexError):
                    continue
        return data

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


class Screener:
    def __init__(self, symbols, datafolder):
        self.symbols = symbols
        self.fetcher= Data_fetcher(datafolder)

    def run(self):

        breakout_stocks = []

        for symbol in self.symbols:

            stock = Stock(symbol)

            prices = self.fetcher.fetch_price(symbol)  # got our prices from the csv

            if (len(prices)==0):
                continue
            else:
                stock.set_price(prices)

            if stock.is_breakout():
                breakout_stocks.append(symbol)

        return breakout_stocks

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
    """Run screener computing metrics for 1Y, 2Y, 5Y, All Time, RS, and Delivery Analysis."""
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
        d_vols = full_data["DeliveryVolume"]
        d_pcts = full_data["DeliveryPercentage"]

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

        # --- Delivery & Volume Analysis ---
        # We capture Traded Volume (Total) and Delivery Volume/Percentage
        v_total = full_data["Volume"]
        
        # We need at least some delivery data to proceed
        valid_delivery = [v for v in d_vols[-252:] if v > 0]
        if valid_delivery:
            # 1 Year Window
            v_1y = d_vols[-252:]
            vt_1y = v_total[-252:]
            p_1y = d_pcts[-252:]
            
            total_dvol_1y = sum(v_1y)
            total_tvol_1y = sum(vt_1y)
            avg_daily_dvol_1y = total_dvol_1y / len(v_1y)
            avg_daily_tvol_1y = total_tvol_1y / len(vt_1y)
            avg_daily_pct_1y = sum(p_1y) / len(p_1y)

            # Observations for thresholds
            weekly_dvol_threshold = total_dvol_1y / 52
            monthly_dvol_threshold = total_dvol_1y / 12
            weekly_tvol_threshold = total_tvol_1y / 52
            monthly_tvol_threshold = total_tvol_1y / 12
            
            # Current windows
            v_curr_week = d_vols[-5:]
            v_curr_month = d_vols[-21:]
            vt_curr_week = v_total[-5:]
            vt_curr_month = v_total[-21:]
            p_curr_week = d_pcts[-5:]
            p_curr_month = d_pcts[-21:]

            # Current Observation Calculations
            curr_vol_daily = d_vols[-1]
            curr_tvol_daily = v_total[-1]
            curr_pct_daily = d_pcts[-1]
            
            curr_vol_weekly = sum(v_curr_week)
            curr_tvol_weekly = sum(vt_curr_week)
            curr_pct_weekly_avg = sum(p_curr_week) / len(p_curr_week) if p_curr_week else 0
            
            curr_vol_monthly = sum(v_curr_month)
            curr_tvol_monthly = sum(vt_curr_month)
            curr_pct_monthly_avg = sum(p_curr_month) / len(p_curr_month) if p_curr_month else 0

            # Matches - Delivery
            row["Delivery % Higher Annual"] = curr_pct_daily > avg_daily_pct_1y
            row["Delivery Vol Higher Annual"] = curr_vol_daily > avg_daily_dvol_1y
            row["Weekly Delivery % > Avg"] = curr_pct_weekly_avg > avg_daily_pct_1y
            row["Weekly Delivery Vol > Avg"] = curr_vol_weekly > weekly_dvol_threshold
            row["Monthly Delivery % > Avg"] = curr_pct_monthly_avg > avg_daily_pct_1y
            row["Monthly Delivery Vol > Avg"] = curr_vol_monthly > monthly_dvol_threshold
            
            # Matches - Traded Volume
            row["Volume Higher Annual"] = curr_tvol_daily > avg_daily_tvol_1y
            row["Weekly Volume > Avg"] = curr_tvol_weekly > weekly_tvol_threshold
            row["Monthly Volume > Avg"] = curr_tvol_monthly > monthly_tvol_threshold
            
            # Values for rendering
            row["Curr Delivery %"] = round(curr_pct_daily, 2)
            row["Curr Delivery Vol"] = round(curr_vol_daily, 0)
            row["Curr Traded Vol"] = round(curr_tvol_daily, 0)
        else:
            # Fallback
            for k in ["Delivery % Higher Annual", "Delivery Vol Higher Annual", "Weekly Delivery % > Avg", 
                      "Weekly Delivery Vol > Avg", "Monthly Delivery % > Avg", "Monthly Delivery Vol > Avg",
                      "Volume Higher Annual", "Weekly Volume > Avg", "Monthly Volume > Avg"]:
                row[k] = False
            row["Curr Delivery %"] = 0
            row["Curr Delivery Vol"] = 0
            row["Curr Traded Vol"] = 0

        results.append(row)

    return results


def download_bhavcopies(days=365):
    import urllib.request
    import urllib.error
    from datetime import datetime, timedelta
    
    folder = "delivery_data"
    os.makedirs(folder, exist_ok=True)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    current_date = start_date
    success_count = 0
    fail_count = 0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    while current_date <= end_date:
        if current_date.weekday() < 5:
            date_str = current_date.strftime("%d%m%Y")
            url = f"https://archives.nseindia.com/products/content/sec_bhavdata_full_{date_str}.csv"
            file_path = os.path.join(folder, f"sec_bhavdata_full_{date_str}.csv")
            
            if not os.path.exists(file_path):
                req = urllib.request.Request(url, headers=headers)
                try:
                    with urllib.request.urlopen(req, timeout=10) as response, open(file_path, 'wb') as out_file:
                        data = response.read()
                        out_file.write(data)
                        success_count += 1
                except urllib.error.HTTPError as e:
                    fail_count += 1
                except Exception as e:
                    fail_count += 1
        
        current_date += timedelta(days=1)
        
    return success_count, fail_count

def merge_delivery_data(data_dir="data", delivery_dir="delivery_data"):
    from datetime import datetime
    
    if not os.path.exists(delivery_dir) or not os.path.exists(data_dir):
        return 0
        
    # 1. Build dictionary of delivery data keyed by (symbol, date) once
    delivery_map = {}
    
    for file in os.listdir(delivery_dir):
        if not file.endswith(".csv"): continue
        filepath = os.path.join(delivery_dir, file)
        
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # normalize keys as NSE csv might have spaces like ' DATE1'
                row_clean = {k.strip(): v.strip() for k,v in row.items() if k is not None}
                
                series = row_clean.get("SERIES", "")
                if series not in ["EQ", "BE", "SM"]: continue
                
                sym = row_clean.get("SYMBOL")
                date_raw = row_clean.get("DATE1")
                deliv_qty = row_clean.get("DELIV_QTY", "")
                deliv_per = row_clean.get("DELIV_PER", "")
                
                if not sym or not date_raw: continue
                
                # Normalize dates: 'DD-MMM-YYYY' -> 'YYYY-MM-DD'
                try:
                    date_obj = datetime.strptime(date_raw, "%d-%b-%Y")
                    date_norm = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    continue
                
                delivery_map[(sym, date_norm)] = {
                    "DeliveryVolume": deliv_qty if deliv_qty != "-" else "",
                    "DeliveryPercentage": deliv_per if deliv_per != "-" else ""
                }
                
    if not delivery_map:
        return 0
        
    stocks_updated = 0
    
    # 2. Loop through all stock CSVs to merge efficiently
    for file in os.listdir(data_dir):
        if not file.endswith(".csv"): continue
        if file.startswith("^"): continue # skip indices
        
        symbol_base = file.replace(".csv", "").replace(".NS", "")
        filepath = os.path.join(data_dir, file)
        
        with open(filepath, 'r') as f:
            lines = list(csv.reader(f))
            
        if not lines or len(lines) < 4: continue
        
        if len(lines[0]) >= 6 and "Price" in lines[0][0]:
            # Append two new columns if not already there
            if "DeliveryVolume" not in lines[0]:
                lines[0].extend(["DeliveryVolume", "DeliveryPercentage"])
                lines[1].extend([symbol_base, symbol_base])
                lines[2].extend(["", ""])
                
            vol_idx = lines[0].index("DeliveryVolume")
            per_idx = lines[0].index("DeliveryPercentage")
                
            for i in range(3, len(lines)):
                row = lines[i]
                if not row: continue
                
                date_val = row[0].strip()
                key = (symbol_base, date_val)
                
                qty = delivery_map.get(key, {}).get("DeliveryVolume", "")
                pct = delivery_map.get(key, {}).get("DeliveryPercentage", "")
                    
                if len(row) < len(lines[0]):
                    row.extend([qty, pct])
                else:
                    row[vol_idx] = qty
                    row[per_idx] = pct
            
            # Overwrite updated CSVs back
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(lines)
            stocks_updated += 1
            
    return stocks_updated


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

    # --- got all the required data so getting screener requirements ---

    screener = Screener(symbols, datafolder)

    result = screener.run()

    with open("screener_output.csv", mode="w", newline="") as file:

        writer = csv.writer(file)
        writer.writerow(["Symbol"])

        for symbol in result:
            writer.writerow([symbol])

    print("Items filtered and Listed in screener_output.csv")
