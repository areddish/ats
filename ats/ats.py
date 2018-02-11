from ibapi import wrapper
from ibapi.client import EClient
from ibapi.contract import ContractDetails

from assets import *
import orders

from threading import Thread, Event
import logging
import argparse


class BrokerPlatform(wrapper.EWrapper, EClient):
    def __init__(self, port, client_id):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)        
        self.client_id = client_id
        self.port = port

    def error(self, reqId:int, errorCode:int, errorString:str):
        super().error(reqId, errorCode, errorString)
        pass

    def connect(self):
        super().connect("127.0.0.1", self.port, self.client_id)
        self.thread = Thread(target = self.run)
        self.thread.start()

    def connectAck(self):        
        print ("Connected!")

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        orders.next_valid_order_id = orderId

        # Until we get this notification we aren't really ready to run
        # the rest of the system live.
        #
        # Now we are ready and really connected.

    def find_contract(self, symbol):
        asset = Stock(symbol)
        self.reqContractDetails(33, asset)

    def contractDetails(self, reqId:int, contractDetails:ContractDetails):
        super().contractDetails(reqId, contractDetails)
        pass

    def contractDetailsEnd(self, reqId:int):
        super().contractDetailsEnd(reqId)
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

    sym = "a"
    while (sym != "" and trader.isConnected()):
        print ("Enter symbol")
        sym = input()
        trader.find_contract(sym)
        ## look up sym
    
    trader.disconnect()
