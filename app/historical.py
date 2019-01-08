# Historical Data Download utility
#
# Given a date range and a symbol it will collect data about that symbol
import argparse
import datetime
import time
import threading
import os
from ats.ats import BrokerPlatform
from ats.assets import Stock
from ats.requests import HistoricalDataRequest

# TIMES are in EST
DELTA_OFFSET = ((datetime.datetime.now(datetime.timezone.utc).astimezone().utcoffset().seconds / 3600) - 19.0) * 60 * 60


def is_weekday(dt):
    return dt.weekday() < 5


def is_before_open(dt):
    open_dt = datetime.datetime(
        dt.year, dt.month, dt.day, 9, 30, 0) + datetime.timedelta(seconds=DELTA_OFFSET)
    return dt < open_dt


def previous_end_of_day(dt):
    return datetime.datetime(dt.year, dt.month, dt.day, 16, 0, 0) - datetime.timedelta(days=1) + datetime.timedelta(seconds=DELTA_OFFSET)


def skip_back_to_next_weekday(dt):
    while (not is_weekday(dt)):
        dt = dt - datetime.timedelta(days=1)
    return dt


def to_ib_timestr(dt):
    return dt.strftime("%Y%m%d %H:%M:%S")


def to_duration(dt_start, dt_end):
    return f"{(dt_end - dt_start).seconds} S"


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
                            type=datetime.datetime, help="Start time", dest="start", default=datetime.datetime.now())
    arg_parser.add_argument("-e", "--end", action="store", type=datetime.datetime,
                            help="End time", dest="end", default=datetime.datetime.now())
    args = arg_parser.parse_args()

    if (DELTA_OFFSET != 0):
        print ("Lame but this app is hard coded to EST.")
        raise EnvironmentError

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

    print(f"Collecting data for {args.symbol} from {args.start if args.start else 'MAX'} - {args.end}")

    try:
        broker = BrokerPlatform(args.port, args.id, use_pace_api=True)        
        broker.connect()

        start = args.start

        print(f"Requesting 1 bar days from {start.strftime('%m-%d-%Y')}")
        request = HistoricalDataRequest(Stock(args.symbol), start, "3 D", "1 min")
        request.set_data_folder(symbol_dir)
        broker.handle_request(request)

    except KeyboardInterrupt:
        print("Interrupt! Closing...")

    print("Done!")
    broker.disconnect()

