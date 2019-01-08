import os
import datetime

from ..assets import Stock
from .request import Request


class HistoricalDataRequest(Request):
    def __init__(self, contract, end_date, duration="1 D", bar_size="1 min", id=None):
        super().__init__(contract)
        self.bars = []
        self.end = end_date
        self.symbol = contract.symbol
        self.duration = duration
        self.bar_size = bar_size
        self.id = id
        self.earliest_date_received = end_date
        self.expected_bars = self._count_of_bars(duration, bar_size)

    def _count_of_bars(self, duration, size):
        # assume 5 S bars
        divisor = 5
        if (size.lower() == "1 min"):
            divisor = 60
        elif (size.lower() == "1 day"):
            divisor = 60 * 60 * 24

        parts = duration.split(" ")
        count = int(parts[0])
        if (parts[1].upper() == "D"):
            unit_to_seconds = 60 * 60 * 24

        duration_in_seconds = count * unit_to_seconds
        return duration_in_seconds // divisor

    def set_data_folder(self, folder):
        self.folder = folder

    def on_error(self, error_code, errorString):
        # Historical Market Data Service error message:HMDS query returned no data: GE@SMART Trades
        if (error_code == 162):
            print("Error 162: ", errorString)

        return False

    def on_data(self, **kwargs):
        assert self.request_id == kwargs["reqId"]
        
        bar = kwargs["bar"]

        bar_date = datetime.datetime.fromtimestamp(int(bar.date))
        self.earliest_date_received = min(self.earliest_date_received, bar_date)
        print ("Historical: recv", bar_date, bar)
        self.bars.append(bar)
        print(f"recv: {len(self.bars)}/{self.expected_bars}")
        if len(self.bars) == self.expected_bars:
            self.complete(**{ "start": None, "end": None})

    def complete(self, **kwargs):
        super().complete(**kwargs)

        print("Complete:", kwargs["start"], "-", kwargs["end"])
        print(f"Earliest bar received: {self.earliest_date_received}")

        if self.folder:
            with open(os.path.join(self.folder, f"{self.symbol}-{self.end.strftime('%m-%d-%Y')}.txt"), "wt") as data_file:
                print(f"Symbol: {self.symbol} {self.contract.localSymbol}", file=data_file)
                for b in self.bars:
                    print(f"{b.date} {b.open} {b.high} {b.low} {b.close} {b.volume} {b.barCount}", file=data_file)
        