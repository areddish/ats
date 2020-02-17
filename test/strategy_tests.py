import unittest
from unittest.mock import MagicMock

#import datetime
from ats.ats import BrokerPlatform
from ats.strategies.bollinger_bandwidth import BollingerBandwithStrategy, Indicators
from ats.assets import Stock
from ats.orders import OrderManager

# from ats.barutils import BarAggregator, BarData
# from ibapi.common import BarData


class TestBollingerBandStrategy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trader = BrokerPlatform(-1, -1)
        cls.trader.order_manager.next_valid_order_id = 1
        cls.trader.APP_NAME = "unit test"
        
    def _create_bar(self, percent, upper=80, middle=60, lower=40):
        return {
            "indicators":
            {
                Indicators.BollingerBands: {
                    24: {
                        "upper": upper,
                        "middle": middle,
                        "lower": lower,
                        "percent": percent
                    }
                }
            }
        }

    def test_buy_condition_rising(self):
        contract = Stock("UNIT")
        strat = BollingerBandwithStrategy(contract, 1000)

        self.assertFalse(strat.check_buy_condition(self._create_bar(0.10)))
        self.assertFalse(strat.check_buy_condition(self._create_bar(0.19)))
        self.assertTrue(strat.check_buy_condition(self._create_bar(0.20)))

    def test_buy_condition_dip(self):
        contract = Stock("UNIT")
        strat = BollingerBandwithStrategy(contract, 1000)

        self.assertFalse(strat.check_buy_condition(self._create_bar(0.20)))
        self.assertFalse(strat.check_buy_condition(self._create_bar(0.19)))
        self.assertTrue(strat.check_buy_condition(self._create_bar(0.20)))
        self.assertFalse(strat.check_buy_condition(self._create_bar(0.19)))

    def test_buy_condition_falling(self):
        contract = Stock("UNIT")
        strat = BollingerBandwithStrategy(contract, 1000)

        self.assertFalse(strat.check_buy_condition(self._create_bar(0.20)))
        self.assertFalse(strat.check_buy_condition(self._create_bar(0.20)))
        self.assertFalse(strat.check_buy_condition(self._create_bar(0.20)))
        self.assertFalse(strat.check_buy_condition(self._create_bar(0.19)))
        self.assertFalse(strat.check_buy_condition(self._create_bar(0.15)))

    def test_order(self):
        contract = Stock("UNIT")
        strat = BollingerBandwithStrategy(contract, 1000)
        strat.run(self.trader)
        strat.open_position(self._create_bar(0.25))
        self.assertTrue(strat.order_placed)

if "__main__" == __name__:
    unittest.main()
