## Data Download utility
## 
## Given a date range and a symbol it will collect data about that symbol
import argparse
import datetime
from ats.ats import BrokerPlatform

def record_bar(bar):
    pass

if "__main__" == __name__:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int,
                            help="TCP port to connect to", dest="port", default=7496)
    arg_parser.add_argument("-i", "--id", action="store",
                            type=int, help="Client ID", dest="id", default=6000)
    arg_parser.add_argument("-d", "--data", action="store", type=str, help="Directory of data", dest="data_dir", default=".") 
    arg_parser.add_argument("-c", "--contract", action="store", type=str, help="Contract symbol", dest="symbol", default="SPX")  
    arg_parser.add_argument("-s", "--start", action="store", type=datetime.datetime, help="Start time", dest="start", default=None)     
    arg_parser.add_argument("-e", "--end", action="store", type=datetime.datetime, help="End time", dest="end", default=datetime.datetime.now())  
    args = arg_parser.parse_args()

    print("Data Collection Tool")
    print(f"Storing data in: {args.data_dir}\{args.symbol}")
    print(f"Collecting data for {args.symbol} from {args.start if args.start else 'MAX'} - {args.end}")

    broker = BrokerPlatform(args.port, args.id, args.data_dir)

    #broker.data_manager.create_download()