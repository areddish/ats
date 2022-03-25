from .request import Request
from ibapi.ticktype import TickTypeEnum

class RealTimeMarketSubscription(Request):
    def __init__(self, contract, is_snapshot=False):
        super().__init__(contract, is_synchronous=is_snapshot)
        self.is_snapshot = is_snapshot

    def on_data(self, **kwargs):
        #assert self.request_id == kwargs["reqId"]

        #print (f"Tick:", kwargs)
        pass
    
    def complete(self, **kwargs):
        # Called when subscription cancelled
        print (f"Cancelling: {self.request_id} for {self.contract.symbol}")

    def on_error(self, error_code, errorString):
        # We didn't handle it, outer error handler should process.
        print (self.__class__.__name__, f"ERROR: {error_code}: {errorString}")
        return False


class SnapshotQuote(RealTimeMarketSubscription):
    def __init__(self, contract):
        super().__init__(contract, is_snapshot=True)
        self.bid = 0
        self.bid_size = 0
        self.ask = 0
        self.ask_size = 0
        self.last = 0
        self.last_size = 0
        self.volume = 0
        self.high = 0
        self.low = 0
        self.is_halted = False

    def on_data(self, **kwargs):
        #assert self.request_id == kwargs["reqId"]

        type = kwargs.get("tickType", -1)
        if type == 0:
            self.bid_size = kwargs["size"]
        elif type == 3:
            self.ask_size = kwargs["size"]
        elif type == 5:
            self.last_size = kwargs["size"]
        elif type == 1:
            self.bid = kwargs["price"]
        elif type == 2:
            self.ask = kwargs["price"]
        elif type == 4:
            self.last = kwargs["price"]
        elif type == 6:
            self.high = kwargs["price"]
        elif type == 7:
            self.low = kwargs["price"]
        elif type == 8:
            self.volume = kwargs["size"]
        elif type == 49:
            self.is_halted = kwargs["value"] > 0

    def complete(self, **kwargs):
        # Called when subscription cancelled
        pass

    def on_error(self, error_code, errorString):
        # We didn't handle it, outer error handler should process.
        print (self.__class__.__name__, f"ERROR: {error_code}: {errorString}")
        return False

class DelayedSnapshotQuote(RealTimeMarketSubscription):
    def __init__(self, contract):
        super().__init__(contract, is_snapshot=True)
        self.bid = 0
        self.bid_size = 0
        self.ask = 0
        self.ask_size = 0
        self.last = 0
        self.last_size = 0
        self.volume = 0
        self.high = 0
        self.low = 0
        self.is_halted = False

    def on_data(self, **kwargs):
        #assert self.request_id == kwargs["reqId"]

        type = kwargs.get("tickType", -1)
        if type == TickTypeEnum.DELAYED_BID_SIZE:
            self.bid_size = kwargs["size"]
        elif type == TickTypeEnum.DELAYED_ASK_SIZE:
            self.ask_size = kwargs["size"]
        elif type == TickTypeEnum.DELAYED_LAST_SIZE:
            self.last_size = kwargs["size"]
        elif type == TickTypeEnum.DELAYED_BID:
            self.bid = kwargs["price"]
        elif type == TickTypeEnum.DELAYED_ASK:
            self.ask = kwargs["price"]
        elif type == TickTypeEnum.DELAYED_LAST:
            self.last = kwargs["price"]
        elif type == TickTypeEnum.DELAYED_HIGH:
            self.high = kwargs["price"]
        elif type == TickTypeEnum.DELAYED_LOW:
            self.low = kwargs["price"]
        elif type == TickTypeEnum.DELAYED_VOLUME:
            self.volume = kwargs["size"]
        elif type == 49:
            self.is_halted = kwargs["value"] > 0
        elif type == 9: # close
            self.last = kwargs["price"]

    def complete(self, **kwargs):
        # Called when subscription cancelled
        pass

    def on_error(self, error_code, errorString):
        # We didn't handle it, outer error handler should process.
        print (self.__class__.__name__, f"ERROR: {error_code}: {errorString}")
        return False
