import os
import argparse
import time

from ats.ats import BrokerPlatform
from ats.barmanager import BarManager
from ats.assets import Stock, Future
from ats.requests import ContractDetailsRequest

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

        #trader.reqMktData(12, Stock("SPY"), "", False, False, [])

        # print("requesting bars")
        # trader.reqRealTimeBars(1, SP500, 5, "TRADES", True, [])
        # trader.reqRealTimeBars(2, Stock("SPY"), 5, "TRADES", True, [])
        # trader.reqRealTimeBars(3, Stock("TNA"), 5, "TRADES", True, [])
        # #trader.reqRealTimeBars(23, Stock("MSFT"), 5, "BID", True, [])
        # #trader.reqRealTimeBars(24, Stock("AAPL"), 5, "TRADES", True, [])
        #trader.reqRealTimeBars(25, Future("ES"), 5, "TRADES", True, [])

        # sym = "a"
        # while (sym != "" and trader.isConnected()):
        time.sleep(5)

        print ("Subscribing.... ")
        bar_man = BarManager(trader)

        esdec21 = Future("ES")
        esdec21.lastTradeDateOrContractMonth = "201812"
        bar_man.subscribe(esdec21)

        time.sleep(60)
    except KeyboardInterrupt:
        print("Interrupt! Closing...")
    #     print ("Enter symbol")
    #     sym = input()
    #     trader.find_contract(sym)

    print("Sending Disconnect. ")
    print("Waiting for disconnect...")
    trader.disconnect()
    print("Goodbye")
