import unittest
import datetime
from ats.assets import Stock, Index, Option, Future, Forex
from ats.barutils import BarAggregator, BarData, barDataToDataFrame
from ibapi.common import BarData

bar_received = False

def to_timestamp(dt):
    return int((dt - datetime.datetime(1970, 1, 1)).total_seconds())


class TestAssets(unittest.TestCase):
    def __create_expanding_bar(self, time, x, low=None):
        bar1 = BarData()
        bar1.time = time
        bar1.date = time
        bar1.open = x
        bar1.high = x+1
        bar1.low = -x if not low else low
        bar1.close = -x-1
        bar1.volume = 1
        bar1.average = 0.
        bar1.hasGaps = ""
        bar1.barCount = 0
        return barDataToDataFrame(bar1)

    def test_bar_high(self):
        bar_agg = BarAggregator(Stock("MSFT"))

        start_time = to_timestamp(datetime.datetime(2018, 10, 18, 9, 0, 0))
        for x in range(4):
            bar1 = self.__create_expanding_bar(start_time, x)
            bar_agg.add_bar(bar1)
            start_time += 5

        self.assertEqual(bar_agg.current_bar.iloc[0].high, 4)

        bar1 = BarData()
        bar1.time = start_time
        bar1.date = start_time
        bar1.high = 4000        
        bar_agg.add_bar(barDataToDataFrame(bar1))
    
        self.assertEqual(bar_agg.current_bar.iloc[0].high, 4000)

    def test_bar_low(self):
        bar_agg = BarAggregator(Stock("MSFT"))

        start_time = to_timestamp(datetime.datetime(2018, 10, 18, 9, 0, 0))
        for x in range(4):
            bar1 = self.__create_expanding_bar(start_time, x, low = 100-x)
            bar_agg.add_bar(bar1)
            start_time += 5

        self.assertEqual(bar_agg.current_bar.iloc[0].low, 97)

        bar1 = BarData()
        bar1.time = start_time
        bar1.date = start_time
        bar1.low = 42
        bar_agg.add_bar(barDataToDataFrame(bar1))
    
        self.assertEqual(bar_agg.current_bar.iloc[0].low, 42)

    def test_bar_accumulates_volume(self):        
        bar_agg = BarAggregator(Stock("MSFT"))

        start_time = to_timestamp(datetime.datetime(2018, 10, 18, 9, 0, 0))
        for x in range(4):
            bar1 = self.__create_expanding_bar(start_time, x)
            bar_agg.add_bar(bar1)
            start_time += 5

        self.assertEqual(bar_agg.current_bar.iloc[0].volume, 4)

        bar1 = BarData()
        bar1.time = start_time        
        bar1.date = start_time
        bar1.volume = 26
        bar_agg.add_bar(barDataToDataFrame(bar1))
    
        self.assertEqual(bar_agg.current_bar.iloc[0].volume, 30)

    def test_5s_to_1min(self):
        global bar_received        
        bar_received = False

        def callback(bar, all_bars):
            global bar_received
            print("Foo")
            bar_received = True

        bar_agg = BarAggregator(Stock("MSFT"), 60, callback=callback)

        start_time = to_timestamp(datetime.datetime(2018, 10, 18, 9, 0, 0))
        for x in range(0, 13):
            print("time", start_time)
            bar1 = BarData()
            bar1.time = start_time
            bar1.date = start_time
            bar1.open = x
            bar1.high = x+1
            bar1.low = -x
            bar1.close = -x-1
            bar1.volume = 1
            bar1.average = 0.
            bar1.hasGaps = ""
            bar1.barCount = 0
            bar_agg.add_bar(barDataToDataFrame(bar1))
            start_time += 5
        self.assertTrue(bar_received)
        #assert bar_received

    def test_offset_start(self):
        global bar_received        
        bar_received = False

        def callback(bar, all_bars):
            global bar_received
            print("Foo")
            bar_received = True

        bar_agg = BarAggregator(Stock("MSFT"), 60, callback=callback)

        start_time = to_timestamp(datetime.datetime(2018, 10, 18, 9, 0, 20))
        for x in range(0, 20):
            print("time", start_time)
            bar1 = BarData()
            bar1.time = start_time
            bar1.date = start_time
            bar1.open = x
            bar1.high = x+1
            bar1.low = -x
            bar1.close = -x-1
            bar1.volume = 1
            bar1.average = 0.
            bar1.hasGaps = ""
            bar1.barCount = 0
            bar_agg.add_bar(barDataToDataFrame(bar1))
            start_time += 5
        self.assertTrue(bar_received)

    def test_5s_to_5min(self):
        global bar_received        
        bar_received = False

        def callback(bar, all_bars):
            global bar_received
            print("Foo")
            bar_received = True

        bar_agg = BarAggregator(Stock("MSFT"), 5 * 60, callback=callback)

        start_time = to_timestamp(datetime.datetime(2018, 10, 18, 9, 0, 0))
        for x in range(0, 5*61):
            print("time", start_time)
            bar1 = BarData()
            bar1.time = start_time
            bar1.date = start_time
            bar1.open = x
            bar1.high = x+1
            bar1.low = -x
            bar1.close = -x-1
            bar1.volume = 1
            bar1.average = 0.
            bar1.hasGaps = ""
            bar1.barCount = 0
            bar_agg.add_bar(barDataToDataFrame(bar1))
            start_time += 5
        self.assertTrue(bar_received)
        #assert bar_received
# if "__main__" == __name__:
#     unittest.main()
