from ibapi.common import BarData

import datetime

class BarAggregator:
    def __init__(self, contract, data_dir, desiredTimeSpanInSeconds=60):
        self.timeSpanInSeconds = desiredTimeSpanInSeconds
        self.current_bar = None #todo
        self.bars = []
        five_secfile_name = "{}\\{}-{:%m-%d-%Y}-5-seconds.txt".format(data_dir, contract.symbol, datetime.datetime.now())
        one_min_file_name = "{}\\{}-{:%m-%d-%Y}-1-minute.txt".format(data_dir, contract.symbol, datetime.datetime.now())
        self.one_min_file = open(one_min_file_name, "wt")
        self.five_second_file = open(five_secfile_name, "wt")
        print ("Date,Open,High,Low,Close,Volume,Average,BarCount", file=self.one_min_file)
        print ("Date,Open,High,Low,Close,Volume,Average,BarCount", file=self.five_second_file)

    def add_bar(self, bar):
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
                if len(self.bars) == 0:
                    print ("Need bars before:",bar_time)
                self.store_bar(bar, False)

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
        if (isFiveSecondBar):
            print (bar_str, file=self.five_second_file)
            self.five_second_file.flush()
        else:
            self.bars.append(bar)
            print(bar_str, file=self.one_min_file)
            self.current_bar = None
            self.one_min_file.flush()