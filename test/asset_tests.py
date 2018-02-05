import unittest
from ats.assets import stock


class TestAssets(unittest.TestCase):
    def test_primaryExchange(self):
        s = stock.Stock("MSFT")
        self.assertEqual(s.primaryExchange, "NASDAQ")

    def test_symbol(self):
        s = stock.Stock("MSFT")
        self.assertEqual(s.symbol, "MSFT")


if "__main__" == __name__:
    unittest.main()
