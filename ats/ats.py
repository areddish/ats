from ibapi import wrapper
from ibapi.client import EClient
import argparse


class BrokerPlatform(wrapper.EWrapper, EClient):
    def __init__(self, port, client_id):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)        
        self.client_id = client_id
        self.port = port

    def run(self):
        super().connect("127.0.0.1", self.port, self.client_id)

    def connectAck(self):
        print("Connected!")


if "__main__" == __name__:
    print("Starting up...")

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--port", action="store", type=int, help="TCP port to connect to", dest="port", default=7497)
    arg_parser.add_argument("-id", "--id", action="store", type=int, help="Client ID", dest="id", default=1026)

    args = arg_parser.parse_args()

    print("Using Client ID: ", args.id)
    print("Connecting to port: ", args.port)

    trader = BrokerPlatform(args.port, args.id)
    trader.run()
