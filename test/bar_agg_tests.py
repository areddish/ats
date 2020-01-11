import unittest
import datetime
from ats.assets import Stock, Index, Option, Future, Forex
from ats.barutils import BarAggregator, BarData
from ibapi.common import BarData

def to_timestamp(dt):
    return  int((dt - datetime.datetime(1970,1,1)).total_seconds())

class TestAssets(unittest.TestCase):
    def test_5s_to_1min(self):
        bar_agg = BarAggregator(Stock("MSFT"), None, 60, callback = lambda x: print(x))

        start_time = to_timestamp(datetime.datetime(2018, 10, 18, 9, 0, 0))
        for x in range(0,12):
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

if "__main__" == __name__:
    unittest.main()