from ibapi.common import BarData
from .EventGenerator import *

import datetime

class BarAggregator(EventGenerator):
    def __init__(self, contract, data_dir, desiredTimeSpanInSeconds=60, callback=None):
        self.timeSpanInSeconds = desiredTimeSpanInSeconds
        self.current_bar = None #todo
        self.bars = []
        self.callback = callback

        if (data_dir != None):
            five_secfile_name = "{}\\{}-{:%m-%d-%Y}-5-seconds.txt".format(data_dir, contract.symbol, datetime.datetime.now())
            one_min_file_name = "{}\\{}-{:%m-%d-%Y}-1-minute.txt".format(data_dir, contract.symbol, datetime.datetime.now())
            self.one_min_file = open(one_min_file_name, "wt")
            self.five_second_file = open(five_secfile_name, "wt")
            print ("Date,Open,High,Low,Close,Volume,Average,BarCount", file=self.one_min_file)
            print ("Date,Open,High,Low,Close,Volume,Average,BarCount", file=self.five_second_file)
        else:
            self.one_min_file = None
            self.five_second_file = None

    def add_bar(self, bar):
        # assuming we are getting bars in order. need to add protection

        self.store_bar(bar, True)
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
            if bar_time.second == 55:
                if len(self.bars) + 1< self.timeSpanInSeconds // 5:
                    print ("Need bars before:",bar_time)
                self.store_bar(bar, False)
                # this is being done in store_Bar.. why?
                # self.bars.append(bar)
                if (self.callback):
                    self.callback(bar, self.bars)

        elif bar_time.second == 0:
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

    def store_bar(self, bar, isFiveSecondBar):
        bar_str = "{},{},{},{},{},{},{},{}".format(bar.time, bar.open, bar.high, bar.low, bar.close, bar.volume, bar.average, bar.barCount)
        if (isFiveSecondBar and self.five_second_file != None):
            print (bar_str, file=self.five_second_file)
            self.five_second_file.flush()
        elif (self.one_min_file != None):
            self.bars.append(bar)
            print(bar_str, file=self.one_min_file)
            self.current_bar = None
            self.one_min_file.flush()


'''
    Produces a stream of in-order bars, but can handle out of order reception
    i.e. accepts 5s bars
         produces 1 min, but in order
         
'''
class InOrderBarStream:
    def __init__(self):
        pass

    def add_partial_bar(self):
        pass
