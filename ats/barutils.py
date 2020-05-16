from ibapi.common import BarData
from pandas import DataFrame

import datetime


class BarAggregator:
    def __init__(self, contract, desiredTimeSpanInSeconds=60, callback=None, live=True):
        self.timeSpanInSeconds = desiredTimeSpanInSeconds
        self.current_bar = DataFrame()
        self.bars = DataFrame()
        self.callback = callback
        self.back_filling = not live

    def add_bar(self, df):
        # Number of seconds since start of bar
        elapsedSeconds = int((df.index[0] - self.current_bar.index[0]).total_seconds()) if not self.current_bar.empty else 0

        # TODO: Assuming we are getting bars in order. Need to add protection
        if not self.current_bar.empty:
            self.updateCurrentDataFrame(df)
            if elapsedSeconds == self.timeSpanInSeconds - 5:
                self.bars = self.bars.append(self.current_bar, verify_integrity=True)
                if self.callback:
                    self.callback(df, self.bars)
                self.current_bar = DataFrame()
        elif df.index[0].second == 0:
            # start this bar
            self.current_bar = df

    def back_fill(self, bar, bars, cb):
        # Update the callback with the new one
        self.callback = cb
        # Merge the back-filled bars with the new one
        self.bars = self.bars.append(bars, verify_integrity=True)
        self.bars.sort_values(by="date", inplace=True)
        # Fire the call back like we are ready.
        self.callback(bar, self.bars)

    def on_backfill_complete(self, bars):
        print(
            f"Backfill complete: {len(self.bars)} + {len(bars)} = {len(self.bars) + len(bars)}"
        )
        self.bars = sorted(bars + self.bars, key=lambda b: b.time)
        self.back_filling = False

        # TODO: Verify no gaps, this will be hard as we may cross days

    def update_callback(self, callback):
        self.callback = callback

    def updateCurrentDataFrame(self, df):
        current = self.current_bar.iloc[0]
        next_bar = df.iloc[0]

        data = [
            current.open,
            max(current.high, next_bar.high),
            min(current.low, next_bar.low),
            current.volume + next_bar.volume,
            next_bar.close,
        ]
        columns = ["open", "high", "low", "volume", "close"]
        self.current_bar = DataFrame(
            dict(zip(columns, data)), index=self.current_bar.index
        )


### TESTS

## 1. live = True, tests with offset start, on 00 start, verify call back
## 2. live = False, test with offset start, getting mix of historical and regular
## 3. live = False, test in order, with live after backfill complete
## 4. live = False, test callback doesn't fire during historical


def barDataToDataFrame(barData: BarData):
    columns = ["date", "open", "high", "low", "close", "volume"]
    data = [datetime.datetime.fromtimestamp(int(barData.date)), barData.open, barData.high, barData.low, barData.close, barData.volume]
    df = DataFrame(dict(zip(columns,data)), columns=columns, index=[0])
    df.set_index("date", inplace=True)
    return df


def createBarDataFrame(date, open, high, low, close, volume):
    columns = ["date", "open", "high", "low", "close", "volume"]
    dt = datetime.datetime.fromtimestamp(int(date))
    data = [dt, open, high, low, close, volume]
    df = DataFrame(dict(zip(columns, data)), index=[0])
    df.set_index("date", inplace=True)
    return df
