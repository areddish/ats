from .request import Request

class RealTimeMarketSubscription(Request):
    def __init__(self, contract, bar_manager):
        super().__init__(contract, is_synchronous=False)

    def on_data(self, **kwargs):
        assert self.request_id == kwargs["reqId"]

        print (f"Tick:")

    def complete(self, **kwargs):
        # Called when subscription cancelled
        print (f"Cancelling: {self.request_id} for {self.contract.symbol}")

    def on_error(self, error_code, errorString):
        # We didn't handle it, outer error handler should process.
        print (self.__class__, f"ERROR: {error_code}: {errorString}")
        return False
