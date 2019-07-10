import os
import argparse
import time

from ats.ats import BrokerPlatform
from ats.barmanager import BarManager
from ats.assets import Stock, Future
from ats.requests import *

if "__main__" == __name__:
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

    trader = BrokerPlatform(args.port, args.id)
    try:
        trader.connect()

        if (not trader.is_connected):
            print ("Couldn't connect.")
            exit(-1)

        for sym in ["AAPL", "TNA", "MSFT", "SPY", "TSLA", "BAC", "AMZN"]:
            details_req = ContractDetailsRequest(Stock(sym))
            trader.handle_request(details_req)

        print ("Subscribing.... ")
        bar_man = BarManager(trader)

        esdec21 = Future("ES")
        esdec21.lastTradeDateOrContractMonth = "201812"
        bar_man.subscribe(esdec21)

        mkt_sub = RealTimeMarketSubscription(Stock("SPY"))
        trader.handle_request(mkt_sub)

# how to manage session?
# how to get backfill data?
# how to connect barman, strategy, indicators, and broker?

        amzn_strategy = BollingBandPercentStrategy(Stock("AMZN"), bar_man)

        trader.run()
        
        print ("Unsubscribing...")
        bar_man.unsubscribe(esdec21)
        trader.cancel_request(mkt_sub)
    except KeyboardInterrupt:
        print("Interrupt! Closing...")
        print("Sending Disconnect. ")
        print("Waiting for disconnect...")
        trader.disconnect()
    print("Goodbye")
