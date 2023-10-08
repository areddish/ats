import argparse
import datetime

from ats.ats import BrokerPlatform
from ats.barmanager import BarManager
from ats.assets import Stock, Future
from ats.requests import *

from pandas import DataFrame

if "__main__" == __name__:
    print("Contract downloader")
    print("Starting up...")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int,
                            help="TCP port to connect to", dest="port", default=7496)
    arg_parser.add_argument("-i", "--id", action="store",
                            type=int, help="Client ID", dest="id", default=1026)
    args = arg_parser.parse_args()

    print("Using Client ID: ", args.id)
    print("Connecting to port: ", args.port)

    sym = [ "SPY", "DVY" ]

    trader = BrokerPlatform(args.port, args.id, wait_for_account=False)
    try:
        trader.connect()

        for s in sym:
            stock = Stock(s)
            req = ContractDetailsRequest(stock)
            res = trader.handle_request(req)

            contract_details = req.details
            print(req.details["MarketName"])
            
    except KeyboardInterrupt:
        print("Interrupt! Closing...")
        print("Sending Disconnect. ")
        print("Waiting for disconnect...")
    except Exception as error:
        print("Error..", error)

    trader.disconnect()
    print("Goodbye")
