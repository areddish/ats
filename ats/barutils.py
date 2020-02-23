from ibapi.common import BarData

import datetime

class BarAggregator:
    def __init__(self, contract, desiredTimeSpanInSeconds=60, callback=None, live=True):
        self.timeSpanInSeconds = desiredTimeSpanInSeconds
        self.current_bar = None
        self.bars = []
        self.callback = callback
        self.back_filling = not live

    def add_bar(self, bar):
        # assuming we are getting bars in order. need to add protection

        if self.current_bar:
            print ("@@@ agg bar: ")
            # aggregate
            self.current_bar.high = max(self.current_bar.high, bar.high)
            self.current_bar.low = min(self.current_bar.low, bar.low)
            self.current_bar.close = bar.close
            self.current_bar.volume += bar.volume
            self.current_bar.average = bar.average
            self.current_bar.barCount += bar.barCount
            if bar.time.second == 55:
                # if len(self.bars) + 1< self.timeSpanInSeconds // 5:
                #     print ("Need bars before:",bar_time)
                self.bars.append(bar)
                if not self.back_filling and self.callback:
                    self.callback(bar, self.bars)

        elif bar.time.second == 0:
            # start this bar
            print("@@@ New bar")
            new_bar = BarData()
            new_bar.time = bar.time
            new_bar.open = bar.open
            new_bar.high = bar.high
            new_bar.low = bar.low
            new_bar.close =bar.close
            new_bar.volume = bar.volume
            new_bar.average = bar.average
            new_bar.barCount = bar.barCount
            self.current_bar = new_bar

    def on_backfill_complete(self, bars):
        print(f"Backfill complete: {len(self.bars)} + {len(bars)} = {len(self.bars) + len(bars)}")
        self.bars = sorted(bars + self.bars, key=lambda b: b.time)
        self.back_filling = False

        # TODO: Verify no gaps, this will be hard as we may cross days


### TESTS

## 1. live = True, tests with offset start, on 00 start, verify call back
## 2. live = False, test with offset start, getting mix of historical and regular
## 3. live = False, test in order, with live after backfill complete
## 4. live = False, test callback doesn't fire during historical
