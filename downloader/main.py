## Data Download utility
## 
## Given a date range and a symbol it will collect data about that symbol
import argparse
import datetime
import time
import threading
import os
from ats.ats import BrokerPlatform
from ats.assets import Stock

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def is_weekday(dt):
    return dt.weekday() < 5

def previous_end_of_day(dt):
    return datetime.datetime(dt.year, dt.month, dt.day, 16, 0, 0) - datetime.timedelta(days=1)
    
def skip_back_to_next_weekday(dt):
    while (not is_weekday(dt)):
        dt = dt - datetime.timedelta(days=1)
    return dt

def to_ib_timestr(dt):
    return dt.strftime("%Y%m%d %H:%M:%S")

def to_duration(dt_start, dt_end):
    return f"{(dt_end - dt_start).seconds} S"

def flush_bars(path, dt, bars):
    with open(os.path.join(path, f"{dt.month}.{dt.day}.{dt.year}.1.minute.txt"),"wt") as file:
        for b in bars:
            file.write(f"{b.date} {b.open} {b.high} {b.low} {b.close} {b.volume} {b.barCount}")
    
if "__main__" == __name__:
    bars = []

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int,
                            help="TCP port to connect to", dest="port", default=7496)
    arg_parser.add_argument("-i", "--id", action="store",
                            type=int, help="Client ID", dest="id", default=6000)
    arg_parser.add_argument("-d", "--data", action="store", type=str, help="Directory of data", dest="data_dir", default=".") 
    arg_parser.add_argument("-c", "--contract", action="store", type=str, help="Contract symbol", dest="symbol", default="AMZN")  
    arg_parser.add_argument("-s", "--start", action="store", type=datetime.datetime, help="Start time", dest="start", default=None)     
    arg_parser.add_argument("-e", "--end", action="store", type=datetime.datetime, help="End time", dest="end", default=datetime.datetime.now())  
    args = arg_parser.parse_args()

    print("Data Collection Tool")
    print(f"Data Directory: {args.data_dir}")

    if (not os.path.exists(args.data_dir)):
        print(f"{args.data_dir} doesn't exist...")
        os.mkdir(args.data_dir, 0x755)
        print(f"Created: {args.data_dir}")

    symbol_dir = os.path.join(args.data_dir, args.symbol)
    print (f"Using: {symbol_dir}")
    if (not os.path.exists(symbol_dir)):
        print(f"{symbol_dir} doesn't exist...")
        os.mkdir(symbol_dir, 0x755)
        print(f"Created: {symbol_dir}")


    print(f"Collecting data for {args.symbol} from {args.start if args.start else 'MAX'} - {args.end}")

    try:
        broker = BrokerPlatform(args.port, args.id, args.data_dir)
        broker.connect()

        def record_bar(bar):
            global bars
            bars.append(bar)

        broker.register_historical_callback(5, record_bar)
        # ask for 1 minute bars starting at start and going til end.
        flush_day = None
        flush_next = False
        current = datetime.datetime(args.end.year, args.end.month, args.end.day, 16, 0, 0)
        start = args.start if args.start else current + datetime.timedelta(weeks=104)
        while (current < start):
            if (flush_next):
                flush_next = False
                flush_bars(symbol_dir, flush_day, bars)
                bars = []

            if (not is_weekday(current)):
                print(f"Skipping non week day: {current.strftime('%m-%d-%Y')} ({WEEKDAYS[current.weekday()]})")
                current = skip_back_to_next_weekday(current)
            else:
                # 4pm, 1pm, 10pm, 9:30
                slice_start = current
                slice_end = current - datetime.timedelta(hours=3)
                if (slice_end.hour < 9):
                    slice_end = datetime.datetime(current.year, current.month, current.day, 9, 30, 0)
                    flush_day = current
                    current = previous_end_of_day(current)
                    flush_next = True
                else: 
                    current = slice_end
                print(f"Requesting: {args.symbol} {slice_start.strftime('%m-%d-%Y: %H:%M:%S')} = {slice_end.strftime('%m-%d-%Y: %H:%M:%S')}")

                broker.reqHistoricalData(5, Stock("AMZN"), to_ib_timestr(slice_end), to_duration(slice_start,slice_end), "1 min", "TRADES", 1, 2, False, "XYZ")
                time.sleep(11)
        #broker.data_manager.create_download()

    except KeyboardInterrupt:
        print ("Interrupt! Closing...")

