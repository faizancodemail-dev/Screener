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
        
        prices = []

        filepath = os.path.join(self.datafolder, f"{symbol}.csv")  # f"{symbol}.csv" == "{}.csv".format(symbol)

        if not os.path.exists(filepath):
            return prices
        else:

            with open(filepath,'r') as file:
                reader = csv.reader(file)

                next(reader)
                next(reader)
                next(reader)

                for row in reader:
                    close_price = float(row[1]) # skipped the indexes and viewed the absolute index of close
                    prices.append(close_price)
                
                return prices
        
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

#----------------------------MAIN------------------------------

if __name__ == "__main__":

    # ---- selecting the time frame and sector ----

    mode = int(input("enter the time frame:"))
    sector = input("enter the sector")



    # ---- getting required data ---- 

    import yfinance as yf

    # getting the list of stock symbols for y finance and formating it to .NS 

    symbols = []

    with open (f'NAMES\\{sector}.csv','r') as file:
        reader = csv.reader(file)

        for row in reader :
            symbols.append(row[0])

    #check if "data" folder exists 

    if not os.path.exists("data"):
        os.makedirs("data")
        print("Created 'data' folder")

        # Loop through each symbol and download 1 year of data
        for symbol in symbols:
            print(f"Downloading data for {symbol}...")
            data = yf.download(symbol, period=f"{mode}y")  # variable year historical data
            file_path = os.path.join("data", f"{symbol}.csv")
            data.to_csv(file_path)
            print(f"Saved {symbol} data to {file_path}")

        print("All downloads complete!")
    else :
        print("Data folder already exists. skipping downloads")



    # --- got all the required data so getting screener requirements ---


    datafolder = 'data'

    screener = Screener(symbols,datafolder)

    result = screener.run()

    with open("screener_output.csv", mode="w", newline="") as file:

        writer = csv.writer(file)
        writer.writerow(["Symbol"])

        for symbol in result:
            writer.writerow([symbol])

    print("Items filtered and Listed in screener_output.csv")
