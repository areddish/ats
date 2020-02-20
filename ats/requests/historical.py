import os
import datetime

from ..assets import Stock
from .request import Request


class HistoricalDataRequest(Request):
    def __init__(self, symbol, end_date, duration="1 D", bar_size="1 min", keep_updated=False, id=None):
        super().__init__(Stock(symbol), is_synchronous=not keep_updated)
        self.bars = []
        self.end = end_date
        self.symbol = symbol
        self.duration = duration
        self.bar_size = bar_size
        self.id = id
        self.earliest_date_received = end_date
        self.keep_updated = keep_updated

    def set_data_folder(self, folder):
        self.folder = folder

    def on_error(self, error_code, errorString):
        # Historical Market Data Service error message:HMDS query returned no data: GE@SMART Trades
        if (error_code == 162):
            print("Error 162: ", errorString)

        return False

    def on_data(self, request_id, bar):
        assert self.request_id == request_id

        bar_date = datetime.datetime.fromtimestamp(int(bar.date))
        self.earliest_date_received = min(
            self.earliest_date_received, bar_date) if self.earliest_date_received else bar_date
        self.bars.append(bar)

    def complete(self, **kwargs):
        # with open(os.path.join(self.folder, f"{self.symbol}-{self.end.strftime('%m-%d-%Y')}.txt"), "wt") as data_file:
        #     for b in self.bars:
        #         print(
        #             f"{b.date} {b.open} {b.high} {b.low} {b.close} {b.volume} {b.barCount}", file=data_file)
        print("Complete:", kwargs["start"], "-", kwargs["end"])