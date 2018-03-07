from ibapi.common import BarData

import datetime

class BarAggregator:
    def __init__(self, desiredTimeSpanInSeconds=60):
        self.timeSpanInSeconds = desiredTimeSpanInSeconds
        self.current_bar = None #todo
        self.bars = []


    def add_bar(self, bar):
        bar_time = datetime.datetime.fromtimestamp(bar.time)
        if self.current_bar:
            print ("@@@ agg bar: ")
            # aggregate
            self.current_bar.high = max(self.current_bar.high, bar.high)
            self.current_bar.low = min(self.current_bar.low, bar.low)
            self.current_bar.close = bar.close
            self.current_bar.volume += bar.volume
            self.current_bar.average = bar.average
            self.current_bar.barCount += bar.barCount
            self.current_bar.hasGaps = self.current_bar.hasGaps or bar.hasGaps
            if bar_time.second == 55:
                print ("Storing bar: ",self.current_bar)
                self.bars.append(self.current_bar)
                self.current_bar = None
        elif bar_time.second == 0:
            # start this bar
            print("@@@ New bar")
            new_bar = BarData()
            new_bar.date = bar.date
            new_bar.open = bar.open
            new_bar.high = bar.high
            new_bar.low = bar.low
            new_bar.close =bar.close
            new_bar.volume = bar.volume
            new_bar.average = bar.average
            new_bar.hasGaps = bar.hasGaps
            new_bar.barCount = bar.barCount
            self.current_bar = new_bar
    