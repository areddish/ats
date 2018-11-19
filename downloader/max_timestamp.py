import datetime
import time
import threading
import os
from ats.ats import BrokerPlatform
from ats.assets import Stock

import argparse

if "__main__" == __name__:

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int,
                            help="TCP port to connect to", dest="port", default=7496)
    arg_parser.add_argument("-i", "--id", action="store",
                            type=int, help="Client ID", dest="id", default=6000)
    arg_parser.add_argument("-d", "--data", action="store", type=str, help="Directory of data", dest="data_dir", default=".") 
    args = arg_parser.parse_args()

    symbols = [ "NFLX", "MSFT", "AMZN", "SPX", "GOOG", "AAPL", "SPY", "TNA", "TSLA" ]

    try:
        broker = BrokerPlatform(args.port, args.id, args.data_dir)
        broker.connect()

        def p(ts):
            print (ts)

        broker.register_historical_callback(35, p)
        for s in symbols:
            print (s,end="")
            broker.reqHeadTimeStamp(35, Stock(s), "TRADES", 1, 2)
            time.sleep(3)

        broker.disconnect()
    except KeyboardInterrupt:
        print ("Interrupt! Closing...")