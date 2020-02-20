import os
import argparse
import time
import datetime

from ats.ats import BrokerPlatform
from ats.barmanager import BarManager
from ats.assets import Stock, Future
from ats.requests import *
from ats.orders import OrderType

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
    print("Order Experimenter")
    print("Starting up...")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int,
                            help="TCP port to connect to", dest="port", default=7497)
    arg_parser.add_argument("-i", "--id", action="store",
                            type=int, help="Client ID", dest="id", default=44443)
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

    trader = BrokerPlatform(args.port, args.id, wait_for_account=False)
    try:
        trader.connect()

        def fill_alert():
            print("ORDER FILLED")

        def cancel_alert():
            print("ORDER CANCELLED")

        if (not trader.is_connected):
            print ("Couldn't connect.")
            exit(-1)

        order = trader.order_manager.create_market_order(Stock("MSFT"), 2, order_type=OrderType.BUY)
        # order.on_fill = fill_alert
        # order.on_cancel = cancel_alert
        order.place()

        #order = trader.order_manager.create_limit_order(Stock("MSFT"), 1000, OrderType.BUY, 186.95)
        #order.place()

        # order2 = trader.order_manager.create_limit_order(Stock("MSFT"), 1, OrderType.SELL, 186)
        # order2.place()

        # order.cancel()
        # order2.update_price(184)

        # m,p,s = trader.order_manager.create_bracket_order(Stock("MSFT"), 1, 186.46, 186.16)
        # m.place()
        # p.place()
        # s.place()

        trader.run()
    except KeyboardInterrupt:
        print("Interrupt! Closing...")
        print("Sending Disconnect. ")
        print("Waiting for disconnect...")

    trader.disconnect()
    print("Goodbye")
