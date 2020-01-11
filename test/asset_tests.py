import unittest
import datetime
from ats.assets import Stock, Index, Option, Future, Forex


class TestAssets(unittest.TestCase):
    def test_primaryExchange(self):
        s = Stock("MSFT")
        self.assertEqual(s.primaryExchange, "NASDAQ")

    def test_symbol(self):
        s = Stock("MSFT")
        self.assertEqual(s.symbol, "MSFT")

    def test_securityType(self):
        self.assertEqual(Stock("MSFT").secType, "STK")
        self.assertEqual(Index("SPX").secType, "IND")
        self.assertEqual(Option("MSFT", expiry=datetime.date.today()).secType, "OPT")
        self.assertEqual(Future("ESH8").secType, "FUT")
        self.assertEqual(Forex("USD.JPY").secType, "CASH")

if "__main__" == __name__:
    unittest.main()
