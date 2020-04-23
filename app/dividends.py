import os
import argparse
import time
import datetime
import math

from ats.ats import BrokerPlatform
from ats.barmanager import BarManager
from ats.assets import Stock, Future
from ats.requests import *

from pandas import DataFrame

def load_tickers():
    tickers = []
    with open("dividends.csv","rt") as file:
        for l in file.readlines()[1:]:
            parts = l.strip().split(",")
            name = parts[0].strip()
            symbol = parts[1].strip()
            if name and symbol:
                tickers.append({ "name": name, "symbol": symbol})

    return sorted(tickers, key=lambda t: t['symbol'])

if "__main__" == __name__:
    print("Dividend Downloader")
    print("Starting up...")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int,
                            help="TCP port to connect to", dest="port", default=7496)
    arg_parser.add_argument("-i", "--id", action="store",
                            type=int, help="Client ID", dest="id", default=1026)
    arg_parser.add_argument("-d", "--data", action="store", type=str,
                            help="Directory of data", dest="data_dir", default=".\\")
    args = arg_parser.parse_args()

    print("Using Client ID: ", args.id)
    print("Connecting to port: ", args.port)
    print("Data directory: ", args.data_dir, end="")

    if (not os.path.isdir(args.data_dir)):
        print("missing!")
        exit(-1)
    else:
        print("exists!")

    dividend_tickers = load_tickers()
    ''' 
   IB Dividends
    tick id 59 Contract's dividends. See IB Dividends
    call back IBApi.EWrapper.tickString
    generic tick type 456
      
    IB Dividends
        This tick type provides four different comma-separated elements:
        The sum of dividends for the past 12 months (0.83 in the example below).
        The sum of dividends for the next 12 months (0.92 from the example below).
        The next dividend date (20130219 in the example below).
        The next single dividend amount (0.23 from the example below).
        Example: 0.83,0.92,20130219,0.23
        
        To receive dividend information it is sometimes necessary to direct-route rather than smart-route market data requests.
    '''

    trader = BrokerPlatform(args.port, args.id, wait_for_account=False)
    try:
        trader.connect()

        # set to delayed
        #trader.client.reqMarketDataType(3)

        if (not trader.is_connected):
            print ("Couldn't connect.")
            exit(-1)

        data = DataFrame(columns=["Symbol", "Last", "Date", "Payout"])
        data.set_index("Symbol", inplace=True)

        for ticker in dividend_tickers:
            print(f"{datetime.datetime.now().strftime('%H:%M:%S.%MS')}: Getting data for {ticker['symbol']}...")

            stock = Stock(ticker['symbol'])
            request = DividendDetailsRequest(stock)
            trader.handle_request(request)
            #print (request.result)

            quote = DelayedSnapshotQuote(stock)
            trader.handle_request(quote)
            data.loc[ticker['symbol']] = [  quote.last, request.next_date, request.next_payout ]

            #df = DataFrame(data, columns=["Symbol","Date","Payout"])
            #df.to_csv("dividend_pays.csv")
            trader.cancel_request(request)
            print(f"{datetime.datetime.now().strftime('%H:%M:%S.%MS')}: {ticker['symbol']} done!")
        
        data.to_csv("dividend_pays.csv")
#         for sym in ["AAPL", "TNA", "MSFT", "SPY", "TSLA", "BAC", "AMZN"]:
#             details_req = ContractDetailsRequest(Stock(sym))
#             trader.handle_request(details_req)

#         print ("Subscribing.... ")
#         bar_man = BarManager(trader)

#         esdec21 = Future("ES")
#         esdec21.lastTradeDateOrContractMonth = "201812"
#         bar_man.subscribe(esdec21)

#         mkt_sub = RealTimeMarketSubscription(Stock("SPY"))
#         trader.handle_request(mkt_sub)

# # how to manage session?
# # how to get backfill data?
# # how to connect barman, strategy, indicators, and broker?

#         amzn_strategy = BollingBandPercentStrategy(Stock("AMZN"), bar_man)
#         print ("Unsubscribing...")
#         bar_man.unsubscribe(esdec21)
#         trader.cancel_request(mkt_sub)
    except KeyboardInterrupt:
        print("Interrupt! Closing...")
        print("Sending Disconnect. ")
        print("Waiting for disconnect...")
    except Exception as error:
        print("Error..", error)

    trader.disconnect()
    print("Goodbye")
