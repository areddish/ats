import os
import datetime

from ..assets import Stock
from .request import Request
from pandas import DataFrame

class HistoricalDataRequest(Request):
    def __init__(self, contract, end_date, duration="1 D", bar_size="1 min", keep_updated=False):
        super().__init__(contract, is_synchronous=not keep_updated)
        self.bars = DataFrame()
        self.end = end_date
        self.duration = duration
        self.bar_size = bar_size
        self.keep_updated = keep_updated
        self.on_complete = None

    def set_data_folder(self, folder):
        self.folder = folder

    def on_error(self, error_code, errorString):
        # Historical Market Data Service error message:HMDS query returned no data: GE@SMART Trades
        if (error_code == 162):
            print("Error 162: ", errorString)

        return False

    def on_data(self, request_id, bar):
        assert self.request_id == request_id
        self.bars = self.bars.append(bar, verify_integrity=True)

    def complete(self, **kwargs):
        # with open(os.path.join(self.folder, f"{self.symbol}-{self.end.strftime('%m-%d-%Y')}.txt"), "wt") as data_file:
        #     for b in self.bars:
        #         print(
        #             f"{b.date} {b.open} {b.high} {b.low} {b.close} {b.volume} {b.barCount}", file=data_file)
        print("Complete:", kwargs["start"], "-", kwargs["end"])
        if self.on_complete:            
            self.on_complete()
            self.on_complete = None