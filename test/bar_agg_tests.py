import unittest
import datetime
from ats.assets import Stock, Index, Option, Future, Forex
from ats.barutils import BarAggregator, BarData
from ibapi.common import BarData


def to_timestamp(dt):
    return int((dt - datetime.datetime(1970, 1, 1)).total_seconds())


class TestAssets(unittest.TestCase):
    def __create_expanding_bar(self, time, x, low=None):
        bar1 = BarData()
        bar1.time = time
        bar1.open = x
        bar1.high = x+1
        bar1.low = -x if not low else low
        bar1.close = -x-1
        bar1.volume = 1
        bar1.average = 0.
        bar1.hasGaps = ""
        bar1.barCount = 0
        return bar1

    def test_bar_high(self):

        bar_agg = BarAggregator(Stock("MSFT"), None, 60)

        start_time = to_timestamp(datetime.datetime(2018, 10, 18, 9, 0, 0))
        for x in range(4):
            bar1 = self.__create_expanding_bar(start_time, x)
            bar_agg.add_bar(bar1)
            start_time += 5

        self.assertEqual(bar_agg.current_bar.high, 4)

        bar1 = BarData()
        bar1.time = start_time
        bar1.high = 4000        
        bar_agg.add_bar(bar1)
    
        self.assertEqual(bar_agg.current_bar.high, 4000)

    def test_bar_low(self):
        bar_agg = BarAggregator(Stock("MSFT"), None, 60)

        start_time = to_timestamp(datetime.datetime(2018, 10, 18, 9, 0, 0))
        for x in range(4):
            bar1 = self.__create_expanding_bar(start_time, x, low = 100-x)
            bar_agg.add_bar(bar1)
            start_time += 5

        self.assertEqual(bar_agg.current_bar.low, 97)

        bar1 = BarData()
        bar1.time = start_time
        bar1.low = 42
        bar_agg.add_bar(bar1)
    
        self.assertEqual(bar_agg.current_bar.low, 42)

    def test_bar_accumulates_volume(self):        
        bar_agg = BarAggregator(Stock("MSFT"), None, 60)

        start_time = to_timestamp(datetime.datetime(2018, 10, 18, 9, 0, 0))
        for x in range(4):
            bar1 = self.__create_expanding_bar(start_time, x)
            bar_agg.add_bar(bar1)
            start_time += 5

        self.assertEqual(bar_agg.current_bar.volume, 4)

        bar1 = BarData()
        bar1.time = start_time
        bar1.volume = 26
        bar_agg.add_bar(bar1)
    
        self.assertEqual(bar_agg.current_bar.volume, 30)

    def test_5s_to_1min(self):
        bar_received = False

        def callback(bar):
            global bar_received
            print ("Callback!")
            bar_received = True

        bar_agg = BarAggregator(Stock("MSFT"), None, 60, callback=callback)

        start_time = to_timestamp(datetime.datetime(2018, 10, 18, 9, 0, 0))
        for x in range(0, 12):
            print("time", start_time)
            bar1 = BarData()
            bar1.time = start_time
            bar1.open = x
            bar1.high = x+1
            bar1.low = -x
            bar1.close = -x-1
            bar1.volume = 1
            bar1.average = 0.
            bar1.hasGaps = ""
            bar1.barCount = 0
            bar_agg.add_bar(bar1)
            start_time += 5
        print (bar_received)
        #assert bar_received


if "__main__" == __name__:
    unittest.main()
