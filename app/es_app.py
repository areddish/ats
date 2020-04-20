import sys
import os
import argparse
import time

from ats.ats import BrokerPlatform
from ats.barmanager import BarManager
from ats.assets import Stock, Future
from ats.requests import *
from ats.strategies import bollinger_bandwidth
from ats.asset_utils import findNearestContractMonth

if "__main__" == __name__:
    print("Starting up...")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int,
                            help="TCP port to connect to", dest="port", default=7496)
    arg_parser.add_argument("-i", "--id", action="store",
                            type=int, help="Client ID", dest="id", default=41026)
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

        es_future = findNearestContractMonth(trader, Future("ES"))

        # bar_man = BarManager(trader)
        # bar_man.subscribe(esdec21)

        strat = bollinger_bandwidth.BollingerBandwithStrategy(es_future, 3400)
        strat.run(trader)

#        amzn_strategy = BollingBandPercentStrategy(Stock("AMZN"), bar_man)
       
        print ("Unsubscribing...")
        # bar_man.unsubscribe(esdec21)
        # trader.cancel_request(mkt_sub)
    except KeyboardInterrupt:
        print("Interrupt! Closing...")
        print("Sending Disconnect. ")
        print("Waiting for disconnect...")
        trader.disconnect()
    except:
        print ("EXCEPTION:", sys.exc_info())
        print("Sending Disconnect. ")
        print("Waiting for disconnect...")
        trader.disconnect()
    print("Goodbye")
