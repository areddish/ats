from .requestmgr import RequestType
from .request import Request
from datetime import datetime

class DividendDetailsRequest(Request):
    def __init__(self, contract):
        super().__init__(contract, True)
        self.request_type = RequestType.DIVIDEND_DETAILS
        self.next_date = None
        self.next_payout = 0

    def on_data(self, **kwargs):

        tick_type = kwargs.get("tickType", -1)
        if tick_type == 59:             
            value = kwargs.get("value", "")
            data = value.split(",")
            '''
                The sum of dividends for the past 12 months (0.83 in the example below).
                The sum of dividends for the next 12 months (0.92 from the example below).
                The next dividend date (20130219 in the example below).
                The next single dividend amount (0.23 from the example below).

                Example: 0.83,0.92,20130219,0.23
            '''
            print("DIVIDENDS: ",tick_type, *data)
            self.next_date = datetime.strptime(data[2], "%Y%m%d")
            self.next_payout = float(data[3])
            self.complete()

    def on_error(self, error_code, errorString):
        # TODO:
        self.next_date = None
        self.next_payout = 0
        self.complete()
        return True