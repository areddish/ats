from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import ContractDetails
from ibapi.common import TickAttrib, BarData

from assets import *
import orders
import barutils

from threading import Thread, Event
import logging
import argparse

import time

bars = 0

class BrokerPlatform(EWrapper, EClient):
    def __init__(self, port, client_id):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)        
        self.client_id = client_id
        self.port = port
        self.baragg = barutils.BarAggregator()

    def error(self, reqId:int, errorCode:int, errorString:str):
        super().error(reqId, errorCode, errorString)
        print(errorCode, errorString)
        pass

    def winError(self, text:str, lastError:int):
        super().winError(text, lastError)
        pass

    def connect(self):
        super().connect("127.0.0.1", self.port, self.client_id)
        self.thread = Thread(target = self.run)
        self.thread.start()
        self.connect_event = Event()
        self.connect_event.wait()

    def connectAck(self):        
        print ("Connected!")

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        print ("Next valid order id", orderId)
        orders.next_valid_order_id = orderId

        # Until we get this notification we aren't really ready to run
        # the rest of the system live.
        #
        # Now we are ready and really connected.
        self.connect_event.set()

    def find_contract(self, symbol):
        asset = Stock(symbol)
        self.reqContractDetails(33, asset)

    def contractDetails(self, reqId:int, contractDetails:ContractDetails):
        super().contractDetails(reqId, contractDetails)
        pass

    def contractDetailsEnd(self, reqId:int):
        super().contractDetailsEnd(reqId)
        pass

    def tickPrice(self, reqId:int , tickType:int, price:float,
                  attrib:TickAttrib):
        print(reqId, tickType, price, attrib)

    def realtimeBar(self, reqId:int, timeStamp:int, open:float, high:float,
                    low:float, close:float, volume:int, wap:float,
                    count: int):
        global bars
        bars += 1
        super().realtimeBar(reqId, timeStamp, open, high, low, close, volume, wap, count)

        b = BarData()
        b.open = open
        b.high = high
        b.time = timeStamp
        b.low = low
        b.close = close
        b.volume = volume
        b.average = wap
        b.barCount = count

        self.baragg.add_bar(b)
        local_time = time.localtime(timeStamp)
        pretty_print_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
        print(reqId, pretty_print_time, high, low, open, close, volume,count," ----", len(self.baragg.bars))
        pass

if "__main__" == __name__:
    print("Starting up...")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int, help="TCP port to connect to", dest="port", default=7496)
    arg_parser.add_argument("-id", "--id", action="store", type=int, help="Client ID", dest="id", default=1026)

    args = arg_parser.parse_args()

    print("Using Client ID: ", args.id)
    print("Connecting to port: ", args.port)

    trader = BrokerPlatform(args.port, args.id)
    trader.connect()

    trader.find_contract("AAPL")

    #trader.reqMktData(12, Stock("SPY"), "", False, False, [])

    print("requesting bars")
    trader.reqRealTimeBars(22, Stock("SPY"), 5, "MIDPOINT", True, [])
    #trader.reqRealTimeBars(23, Stock("MSFT"), 5, "BID", True, [])
    #trader.reqRealTimeBars(24, Stock("AAPL"), 5, "TRADES", True, [])
    #trader.reqRealTimeBars(25, Future("ES"), 5, "MIDPOINT", True, [])

    sym = "a"
    while (sym != "" and trader.isConnected()):
        time.sleep(2)
        #trader.find_contract(sym)
        ## look up sym
    
    trader.disconnect()
