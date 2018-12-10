from .request import Request

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
        print (self.__class__, f"ERROR: {error_code}: {errorString}")
        return False
