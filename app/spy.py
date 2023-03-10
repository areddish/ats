import os
import argparse
import time

from ats.ats import BrokerPlatform
from ats.barmanager import BarManager
from ats.assets import Stock, Future
from ats.requests import *
from ats.strategies.bollinger_bandwidth import BollingerBandwithStrategy

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

        spy = Stock("SPY")
        spy_details = ContractDetailsRequest(spy)
        trader.handle_request(spy_details)

        print(spy_details.details.minTick)
        print ("Subscribing.... ")
        bar_man = BarManager(trader)
        bar_man.subscribe(spy)

        mkt_sub = RealTimeMarketSubscription(Stock("SPY"))
        trader.handle_request(mkt_sub)

        # spy_strategy = BollingerBandwithStrategy(spy, bar_man)
        # strat = BollingerBandwithStrategy(spy, 500, spy_details.details.minTick)

        ## HOW TO EXIT?
        # strat.run(trader)
        trader.run()
        
        print ("Unsubscribing...")
        bar_man.unsubscribe(spy)
        trader.cancel_request(mkt_sub)
    except KeyboardInterrupt:
        print("Interrupt! Closing...")
        print("Sending Disconnect. ")
        print("Waiting for disconnect...")
        trader.disconnect()
    print("Goodbye")
