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

# TIMES are in EST

DELTA_OFFSET = ((datetime.datetime.now(datetime.timezone.utc).astimezone().utcoffset().seconds / 3600) - 19.0) * 60 * 60

def is_weekday(dt):
    return dt.weekday() < 5

def is_before_open(dt):
    open_dt = datetime.datetime(dt.year, dt.month, dt.day, 9, 30, 0) + datetime.timedelta(seconds=DELTA_OFFSET)
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

def flush_bars(path, dt, bars):
    with open(os.path.join(path, f"{dt.month}.{dt.day}.{dt.year}.1.minute.txt"),"wt") as file:
        for b in bars:
            print(f"{b.date} {b.open} {b.high} {b.low} {b.close} {b.volume} {b.barCount}", file=file)


class HistoricalDataRequest:
    def __init__(self, symbol, end_date, duration="1 D", id = None):
        self.bars = []
        self.end = end_date
        self.symbol = symbol
        self.duration = duration
        self.bar_size = "1 min"
        self.id = id
    def set_data_folder(self, folder):
        self.folder = folder

    def on_bar(self, bar):
        self.bars.append(bar)

    def on_request_over(self):
        earliest_date = None
        with open(os.path.join(self.folder, f"{self.symbol}-{self.start.strftime('%m-%d-%Y')}-{self.end.strftime('%m-%d-%Y')}.txt"),"wt") as data_file:
            for b in self.bars:
                bar_date = datetime.datetime.fromtimestamp(int(b.date))
                earliest_date = bar_date if bar_date < earliest_date else bar_date
                print(f"{b.date} {b.open} {b.high} {b.low} {b.close} {b.volume} {b.barCount}", file=data_file)
        self.earliest_date_received = earliest_date

if "__main__" == __name__:
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

    if (DELTA_OFFSET != 0):
        raise EnvironmentError

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
    
        start = datetime.datetime.now()
        while (start.year > 2002):
            print (f"Requesting 30 days from {start.strftime('%m-%d-%Y')}")
            request = HistoricalDataRequest(args.symbol, start, "30 D", id = args.id)                
            request.set_data_folder(symbol_dir)
            broker.queue_request(request)
            start = request.earliest_date_received - datetime.timedelta(days=1)

    except KeyboardInterrupt:
        print ("Interrupt! Closing...")

