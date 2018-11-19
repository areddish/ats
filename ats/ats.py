from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import ContractDetails
from ibapi.common import TickAttrib, BarData

from .assets import *
from .orders import *
from .barutils import *
from .requestmgr import RequestManager
from threading import Thread, Event
import logging
import argparse

import os
import time

import pickle

bars = 0

def to_ib_timestr(dt):
    return dt.strftime("%Y%m%d %H:%M:%S")

def to_duration(dt_start, dt_end):
    return f"{(dt_end - dt_start).seconds} S"

class BrokerPlatform(EWrapper, EClient):
    def __init__(self, port, client_id, data_dir):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.client_id = client_id
        self.port = port
        self.data_dir = data_dir        
        self.bar_series_builder = {}
        self.request_manager = RequestManager()
        self.historical_callbacks = {}
        self.historical_requests = {}
        self.historical_request_next_id = 400

    def error(self, reqId: int, errorCode: int, errorString: str):
        super().error(reqId, errorCode, errorString)
        print(errorCode, errorString)
        pass

    def winError(self, text: str, lastError: int):
        super().winError(text, lastError)
        pass

    def connect(self, host="127.0.0.1"):
        super().connect(host, self.port, self.client_id)
        self.thread = Thread(target=self.run)
        self.thread.start()
        self.connect_event = Event()
        self.connect_event.wait()

    def connectAck(self):
        print("Connected!")

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        print("Next valid order id", orderId)
        #orders.next_valid_order_id = orderId

        # Until we get this notification we aren't really ready to run
        # the rest of the system live.
        #
        # Now we are ready and really connected.
        self.connect_event.set()

    def find_contract(self, contract):
        reqId, event = self.request_manager.create_sync_request()
        self.reqContractDetails(reqId, contract)
        event.wait()

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails)
        print(contractDetails.summary.symbol,
              contractDetails.contractMonth, contractDetails.summary.conId, contractDetails)
        
        print(contractDetails.marketName)
        print(contractDetails.validExchanges)
        print(contractDetails.priceMagnifier)
        print(contractDetails.longName)
        print(contractDetails.industry)
        print(contractDetails.subcategory)
        print(contractDetails.tradingHours)
        print(contractDetails.liquidHours)
        print(contractDetails.summary)        
        
        pickle.dump(contractDetails, open(contractDetails.summary.symbol, "wt"))

    def contractDetailsEnd(self, reqId: int):
        super().contractDetailsEnd(reqId)
        self.request_manager.mark_finished(reqId)
        pass

    def tickPrice(self, reqId: int, tickType: int, price: float,
                  attrib: TickAttrib):
        print(reqId, tickType, price, attrib)

    def queue_request(self, request):
        # historical requests are in the 400 - 500 range
        req_id = self.historical_request_next_id
        self.historical_request_next_id += 1
        request.id = req_id
        self.historical_requests[req_id] = request

        self.reqHistoricalData(req_id, Stock(request.symbol), to_ib_timestr(request.end), to_duration(request.start, request.end), "1 min", "TRADES", 1, 2, False, "XYZ")


    def register_historical_callback(self, reqId, cb):
        self.historical_callbacks[reqId] = cb

    def historicalData(self, reqId, bar):
        if (reqId >= 400):
            self.historical_requests[reqId].on_bar(bar)
        else:
            cb = self.historical_callbacks.get(reqId, None)
            if (not cb):
                print (f"ERROR: No callback for {reqId}")
                raise KeyError

            cb(bar)

    def historicalDataEnd(self, reqId:int, start:str, end:str):
        if (reqId >= 400):
            self.historical_requests[reqId].on_request_over()

    def headTimestamp(self, reqId:int, headTimestamp:str):
        self.historical_callbacks[reqId](headTimestamp)

    def reqRealTimeBars(self, reqId, contract, barSize:int,
                        whatToShow:str, useRTH:bool,
                        realTimeBarsOptions):
        self.bar_series_builder[reqId] = barutils.BarAggregator(contract, self.data_dir)
        super().reqRealTimeBars(reqId, contract, barSize, whatToShow, useRTH, realTimeBarsOptions)
        
    def realtimeBar(self, reqId: int, timeStamp: int, open: float, high: float,
                    low: float, close: float, volume: int, wap: float,
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

        self.bar_series_builder[reqId].add_bar(b)
        local_time = time.localtime(timeStamp)
        pretty_print_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
        print(reqId, pretty_print_time, high, low, open, close,
              volume, count)
        pass


if "__main__" == __name__:
    print("Starting up...")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int,
                            help="TCP port to connect to", dest="port", default=7496)
    arg_parser.add_argument("-i", "--id", action="store",
                            type=int, help="Client ID", dest="id", default=1026)
    arg_parser.add_argument("-d", "--data", action="store", type=str, help="Directory of data", dest="data_dir", default=".\\")    
    args = arg_parser.parse_args()

    print("Using Client ID: ", args.id)
    print("Connecting to port: ", args.port)
    print("Data directory: ", args.data_dir, end="")

    if (not os.path.isdir(args.data_dir)):
        print ("missing!")
        exit(-1)
    else:
        print ("exists!")

    trader = BrokerPlatform(args.port, args.id, args.data_dir)
    trader.connect()

    for sym in ["AAPL", "TNA", "MSFT", "SPY", "TSLA", "BAC", "AMZN"]:
        trader.find_contract(Stock(sym))

    #trader.reqMktData(12, Stock("SPY"), "", False, False, [])

    # print("requesting bars")
    # trader.reqRealTimeBars(1, SP500, 5, "TRADES", True, [])
    # trader.reqRealTimeBars(2, Stock("SPY"), 5, "TRADES", True, [])
    # trader.reqRealTimeBars(3, Stock("TNA"), 5, "TRADES", True, [])
    # #trader.reqRealTimeBars(23, Stock("MSFT"), 5, "BID", True, [])
    # #trader.reqRealTimeBars(24, Stock("AAPL"), 5, "TRADES", True, [])
    trader.reqRealTimeBars(25, Future("ES"), 5, "TRADES", True, [])

    try:
        sym = "a"
        while (sym != "" and trader.isConnected()):
            time.sleep(2)
    except KeyboardInterrupt:
        print ("Interrupt! Closing...")
    #     print ("Enter symbol")
    #     sym = input()
    #     trader.find_contract(sym)

    print ("Sending Disconnect. ")
    trader.disconnect()
    print ("Waiting for disconnect...")
    trader.thread.join()
    print ("Goodbye")