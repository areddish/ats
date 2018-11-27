import datetime
import time
import threading
import os
from ats.ats import BrokerPlatform
from ats.assets import Stock

import argparse

  
class HistoricalHeadTimeStampRequest:
    def __init__(self, broker, symbol):
        self.broker = broker
        self.contract = Stock(symbol)
    
    def make_request(self):
        self.reqId = broker.register_request(self)
        broker.reqHeadTimeStamp(self.reqId, self.contract)

    def on_response(reqId, timestamp):
        if (self.reqId != reqId):
            raise "Invalid request"

        print (timestamp)
        broker.cancelHeadTimeStamp(self.reqId)

if "__main__" == __name__:

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int,
                            help="TCP port to connect to", dest="port", default=7496)
    arg_parser.add_argument("-i", "--id", action="store",
                            type=int, help="Client ID", dest="id", default=6000)
    arg_parser.add_argument("-d", "--data", action="store", type=str, help="Directory of data", dest="data_dir", default=".") 
    args = arg_parser.parse_args()

    symbols = [ "NFLX", "MSFT", "AMZN", "SPX", "GOOG", "AAPL", "SPY", "TNA", "TSLA" ]
    symbols_map = dict(zip(range(len(symbols)), symbols))

    try:
        broker = BrokerPlatform(args.port, args.id, args.data_dir)
        broker.connect()

        def p(ts):
            ts_int = int(ts)
            time = datetime.datetime.fromtimestamp(ts_int)
            print (symbols_map, ts, time.strftime("%m-%d-%Y %H:%M:%S"))
            broker.cancelHeadTimeStamp(35)

        broker.register_historical_callback(35, p)
        for s in zip(symbols, range(len(symboles)):
            print (s,end="")
            broker.reqHeadTimeStamp(35, Stock(s), "TRADES", 1, 2)
            time.sleep(3)

        broker.disconnect()
    except KeyboardInterrupt:
        print ("Interrupt! Closing...")