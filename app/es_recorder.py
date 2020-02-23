import sys
import os
import argparse
import time

from ats.ats import BrokerPlatform
from ats.barmanager import BarManager, BarDb
from ats.assets import Stock, Future
from ats.requests import *
from ats.strategies import bollinger_bandwidth
from ats.util.util import get_data_folder, get_user_file

APP_NAME = "footrader.recorder"
DATA_DIR = get_data_folder(APP_NAME)

if "__main__" == __name__:
    print("Starting up...")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int,
                            help="TCP port to connect to", dest="port", default=7496)
    arg_parser.add_argument("-i", "--id", action="store",
                            type=int, help="Client ID", dest="id", default=41026)
    args = arg_parser.parse_args()

    print("Using Client ID: ", args.id)
    print("Connecting to port: ", args.port)
    print("Data directory: ", DATA_DIR, end="")

    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    es_future = Future("ES")
    # TODO: need a way to find the next forward future 
    #esdec21.find_next_forward_month()
    es_future.lastTradeDateOrContractMonth = "20200320"

#    DB = get_user_file(APP_NAME, f"es-{es_future.lastTradeDateOrContractMonth}.db")
    DB = get_user_file(APP_NAME, f"msft.db")

    db = BarDb(DB)
    bar_man = BarManager(None, db)
    trader = BrokerPlatform(args.port, args.id, bar_manager=bar_man)

    try:
        trader.connect()

        if (not trader.is_connected):
            print ("Couldn't connect.")
            exit(-1)


        bar_man.subscribe_from(Stock("msft"), duration='5 S', end_date=None)
#        bar_man.subscribe(es_future)

        req = HistoricalDataRequest("msft", None, keep_updated=True)
        trader.handle_request(req)
        trader.run()
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
