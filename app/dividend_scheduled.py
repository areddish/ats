import argparse
import psycopg2

from datetime import datetime

from ats.ats import BrokerPlatform
from ats.barmanager import BarManager
from ats.assets import Stock, Future
from ats.requests import *

DB_NAME = "dividends"
class DividendDb():
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def connect(self):
        self.conn = psycopg2.connect(f"dbname={self.db_name} user=postgres password=postgres")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT version()")
        print (self.cur.fetchone())

    def get_all_tickers(self):
        self.cur.execute("SELECT symbol, exchange from dividends")
        return self.cur.fetchall()

    def get_tickers_needing_update(self):
        self.cur.execute("SELECT symbol, exchange FROM public.dividends WHERE next_ex_dividend is NULL or next_ex_dividend < CURRENT_DATE - 3;")
        return self.cur.fetchall()

    def create_table(self):
        create_command = """
            CREATE TABLE IF NOT EXISTS dividends (
                symbol varchar(26) NOT NULL,
                con_id varchar(40),
                exchange varchar(10),
                next_ex_dividend DATE,
                next_payment DECIMAL(19,4),
                PRIMARY KEY (symbol)
            )
        """
        self.cur.execute(create_command)
        self.conn.commit()

    def add_ticker(self, symbol):
        insert_command = f"INSERT INTO public.dividends(symbol) VALUES (%s);"
        self.cur.execute(insert_command, (symbol,))
        self.conn.commit()

    def update_ticker(self, symbol, con_id, exchange, date, price):
        update_command = """
            UPDATE dividends 
                SET con_id=%s,
                exchange=%s,
                next_ex_dividend=%s,
                next_payment=%s
            WHERE symbol=%s
        """
        self.cur.execute(update_command, (con_id, exchange, date, price, symbol))
        self.conn.commit()

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

def update_tickers_db():
    trader = BrokerPlatform(args.port, args.id, wait_for_account=False)
    try:
        trader.connect()
        print ("updating db")
        db = DividendDb()
        db.connect()
    # Creational
    #    db.create_table()
    #    for ticker in load_tickers():
    #        print("Adding:",ticker["symbol"])
    #        db.add_ticker(ticker['symbol'])
        for ticker in db.get_tickers_needing_update():
            print(f"{datetime.now().strftime('%H:%M:%S.%MS')}: Getting data for {ticker[0]}...")
            stock = Stock(ticker[0], primaryExchange=ticker[1] if ticker[1] else None)
            request = DividendDetailsRequest(stock)
            trader.handle_request(request)
            #print (request.result)
            db.update_ticker(ticker[0], None, None, request.next_date, request.next_payout)
            trader.cancel_request(request)
            print(f"{datetime.now().strftime('%H:%M:%S.%MS')}: {ticker[0]} done!")
    except KeyboardInterrupt:
        print("Interrupt! Closing...")
        print("Sending Disconnect. ")
        print("Waiting for disconnect...")
    except Exception as error:
        print("Error..", error)

    trader.disconnect()
    

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int,
                            help="TCP port to connect to", dest="port", default=7496)
    arg_parser.add_argument("-i", "--id", action="store",
                            type=int, help="Client ID", dest="id", default=1026)
    arg_parser.add_argument("-d", "--data", action="store", type=str,
                            help="Directory of data", dest="data_dir", default=".\\")
    args = arg_parser.parse_args()

    print("Scheduled Dividend Retreival: ", datetime.now())
    print("Using Client ID: ", args.id)
    print("Connecting to port: ", args.port)
    print("Data directory: ", args.data_dir, end="")

    update_tickers_db()

    print("Goodbye")



    ##
    ## 2065 200 The contract description specified for CAT is ambiguous.
