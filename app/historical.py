# Historical Data Download utility
##
# Given a date range and a symbol it will collect data about that symbol
import argparse
import datetime
import time
import threading
import os
from ats.ats import BrokerPlatform
from ats.assets import Stock

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']
from ats.requests import HistoricalDataRequest, ContractDetailsRequest

# TIMES are in EST

DELTA_OFFSET = ((datetime.datetime.now(datetime.timezone.utc).astimezone().utcoffset().seconds / 3600) - 19.0) * 60 * 60

if "__main__" == __name__:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int,
                            help="TCP port to connect to", dest="port", default=7496)
    arg_parser.add_argument("-i", "--id", action="store",
                            type=int, help="Client ID", dest="id", default=6000)
    arg_parser.add_argument("-d", "--data", action="store", type=str,
                            help="Directory of data", dest="data_dir", default=".")
    arg_parser.add_argument("-c", "--contract", action="store",
                            type=str, help="Contract symbol", dest="symbol", default="AMZN")
    arg_parser.add_argument("-s", "--start", action="store",
                            type=lambda d: datetime.datetime.strptime(d, "%m-%d-%Y"), help="Start time mm-dd-yyyy", dest="start", default=None)
    arg_parser.add_argument("-e", "--end", action="store", type=lambda d: datetime.datetime.strptime(d, "%m-%d-%Y"),
                            help="End time", dest="end", default=datetime.datetime.now())
    args = arg_parser.parse_args()

    # if (DELTA_OFFSET != 0):
    #     raise EnvironmentError

    print("Data Collection Tool")
    print(f"Data Directory: {args.data_dir}")

    if (not os.path.exists(args.data_dir)):
        print(f"{args.data_dir} doesn't exist...")
        os.mkdir(args.data_dir, 0x755)
        print(f"Created: {args.data_dir}")

    symbol_dir = os.path.join(args.data_dir, args.symbol)
    print(f"Using: {symbol_dir}")
    if (not os.path.exists(symbol_dir)):
        print(f"{symbol_dir} doesn't exist...")
        os.mkdir(symbol_dir, 0x755)
        print(f"Created: {symbol_dir}")

    print(
        f"Collecting data for {args.symbol} from {args.start if args.start else 'MAX'} - {args.end}")

    try:
        broker = BrokerPlatform(args.port, args.id)
        #broker.setConnOptions("+PACEAPI")
        broker.connect()

        start = datetime.datetime.now()
        stock = Stock(args.symbol)

        # Get details on how far back we can go.
        details_req = ContractDetailsRequest(stock)
        broker.handle_request(details_req)

        print(f"Available from:")
        
        current = args.start
        while current > datetime.datetime(2013, 8, 19):
            print(f"Requesting 1 bar days from {current.strftime('%m-%d-%Y')}")
            request = HistoricalDataRequest(Stock(args.symbol), current, duration="5 D")
            request.set_data_folder(symbol_dir)
            broker.handle_request(request)
            request.event.wait()
            current -= datetime.timedelta(days=7)

        broker.disconnect()
        # with open(os.path.join(args.data_dir, f"{args.symbol}-{args.end.strftime('%m-%d-%Y')}.txt"), "wt") as data_file:
        #     for b in request.bars:
        #         print(
        #             f"{b.date},{b.open},{b.high},{b.low},{b.close},{b.volume},{b.barCount}", file=data_file)
    except KeyboardInterrupt:
        print("Interrupt! Closing...")
