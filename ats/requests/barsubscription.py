from .request import Request
from .historical import HistoricalDataRequest

class RealTimeBarSubscription(Request):
    def __init__(self, contract, bar_manager):
        super().__init__(contract, is_synchronous=False)
        self.bar_manager = bar_manager

    def on_data(self, **kwargs):
        assert self.request_id == kwargs["reqId"]

        bar = kwargs["bar"]
        self.bar_manager.on_bar(self.contract, bar)
        print (f"BAR: {bar}")

    def complete(self, **kwargs):
        # Called when subscription cancelled
        print (f"Cancelling: {self.request_id} for {self.contract.symbol}")

    def on_error(self, error_code, errorString):
        # We didn't handle it, outer error handler should process.
        print (self.__class__.__name__, f"ERROR: {error_code}: {errorString}")
        if error_code == 200:
            print (f"Invalid contract specification for {self.contract.symbol} to get bars.")
            return True

        return False

class RealTimeBarSubscriptionWithBackFill(HistoricalDataRequest):
    def __init__(self, contract, end_date, bar_manager):
        super().__init__(contract, end_date, keep_updated=True)
        self.bar_manager = bar_manager
        self.bars = []

    def on_data(self, **kwargs):
        assert self.request_id == kwargs["reqId"]

        bar = kwargs["bar"]
        self.bars.append(bar)
        print (f"BAR: {bar}")

    def complete(self, **kwargs):
        # Called when subscription cancelled
        print (f"Cancelling: {self.request_id} for {self.contract.symbol}")
        self.bar_manager.on_backfill_complete(self.contract, self.bars)

    def on_error(self, error_code, errorString):
        # We didn't handle it, outer error handler should process.
        print (self.__class__.__name__, f"ERROR: {error_code}: {errorString}")
        if error_code == 200:
            print (f"Invalid contract specification for {self.contract.symbol} to get bars.")
            return True

        return False