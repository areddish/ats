from ibapi.ticktype import *
from .request import Request

class PriceSnapshotRequest(Request):
    def __init__(self, contract):
        super().__init__(contract, is_synchronous=True)
        self.bid = 0
        self.ask = 0
        self.last = 0
        self.volume = 0

    def on_data(self, **kwargs):
        #assert self.request_id == kwargs["reqId"]

        type = kwargs.get("tickType", -1)
        value = kwargs.get("price", 0)
        print (f"Tick:", type, value)

        # todo use tick types
        if type == 1:
            self.bid = value
        elif type == 2:
            self.ask = value
        elif type == 4:
            self.last = value

    def complete(self, **kwargs):
        # Called when snapshot over
        print (f"Complete: {self.request_id} for {self.contract.symbol}")
        super().complete()
        
    def on_error(self, error_code, errorString):
        # We didn't handle it, outer error handler should process.
        print (self.__class__.__name__, f"ERROR: {error_code}: {errorString}")
        return False