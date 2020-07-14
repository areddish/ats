import unittest
from unittest.mock import MagicMock

#import datetime
from ats.ats import BrokerPlatform
from ats.strategies.bollinger_bandwidth import BollingerBandwithStrategy, Indicators, BollingerBandwithStrategyState
from ats.assets import Stock
from ats.orders import OrderManager, Order

from ats.sms.twilio import disable_notification

# from ats.barutils import BarAggregator, BarData
# from ibapi.common import BarData

class MockOrderManager(OrderManager):
    def __init__(self, trader):
        pass

    def create_bracket_order(self, contract, qty, profit_price, stop_loss_price):
        return Order(), Order, Order()

    def place_order(self, order):
        pass
    
    
class TestBollingerBandStrategy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trader = BrokerPlatform(-1, -1)
        cls.trader.order_manager.next_valid_order_id = 1
        cls.trader.APP_NAME = "unit test"
        cls.trader.order_manager = MockOrderManager
        disable_notification()

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

    def test_initial(self):
        contract = Stock("UNIT")
        strat = BollingerBandwithStrategy(contract, 1000)
        self.assertTrue(strat.status == BollingerBandwithStrategyState.Looking)

    def test_buy_condition_rising(self):
        contract = Stock("UNIT")
        strat = BollingerBandwithStrategy(contract, 1000)
        
        self.assertTrue(strat.status == BollingerBandwithStrategyState.Looking)
        self.assertFalse(strat.check_open_condition(self._create_bar(0.10)))
        self.assertTrue(strat.status == BollingerBandwithStrategyState.Dipped)
        self.assertFalse(strat.check_open_condition(self._create_bar(0.19)))
        self.assertTrue(strat.check_open_condition(self._create_bar(0.20)))
        self.assertTrue(strat.check_open_condition(self._create_bar(0.22)))

    def test_buy_condition_dip(self):
        contract = Stock("UNIT")
        strat = BollingerBandwithStrategy(contract, 1000)

        self.assertTrue(strat.status == BollingerBandwithStrategyState.Looking)
        self.assertFalse(strat.check_open_condition(self._create_bar(0.20)))
        self.assertTrue(strat.status == BollingerBandwithStrategyState.Looking)
        self.assertFalse(strat.check_open_condition(self._create_bar(0.19)))
        self.assertTrue(strat.status == BollingerBandwithStrategyState.Dipped)
        self.assertTrue(strat.check_open_condition(self._create_bar(0.20)))
        self.assertFalse(strat.check_open_condition(self._create_bar(0.19)))
        self.assertTrue(strat.check_open_condition(self._create_bar(0.21)))
        self.assertTrue(strat.status == BollingerBandwithStrategyState.Dipped)

    def test_buy_condition_falling(self):
        contract = Stock("UNIT")
        strat = BollingerBandwithStrategy(contract, 1000)

        self.assertTrue(strat.status == BollingerBandwithStrategyState.Looking)
        self.assertFalse(strat.check_open_condition(self._create_bar(0.20)))
        self.assertFalse(strat.check_open_condition(self._create_bar(0.20)))
        self.assertFalse(strat.check_open_condition(self._create_bar(0.20)))
        self.assertFalse(strat.check_open_condition(self._create_bar(0.19)))
        self.assertTrue(strat.status == BollingerBandwithStrategyState.Dipped)
        self.assertFalse(strat.check_open_condition(self._create_bar(0.15)))

    def test_short_position_open(self):
        contract = Stock("UNIT")
        strat = BollingerBandwithStrategy(contract, 1000)

        self.assertTrue(strat.status == BollingerBandwithStrategyState.Looking)
        self.assertFalse(strat.check_open_condition(self._create_bar(1.20)))
        self.assertTrue(strat.status == BollingerBandwithStrategyState.Peaked)
        self.assertFalse(strat.check_open_condition(self._create_bar(1.0)))
        self.assertFalse(strat.check_open_condition(self._create_bar(0.9)))
        self.assertFalse(strat.check_open_condition(self._create_bar(0.8)))
        self.assertTrue(strat.check_open_condition(self._create_bar(0.65)))
        self.assertTrue(strat.check_open_condition(self._create_bar(0.65)))
        self.assertTrue(strat.status == BollingerBandwithStrategyState.Peaked)

    def test_short_position_close(self):
        contract = Stock("UNIT")
        strat = BollingerBandwithStrategy(contract, 1000)

        self.assertTrue(strat.status == BollingerBandwithStrategyState.Looking)
        self.assertFalse(strat.check_open_condition(self._create_bar(1.20)))
        self.assertTrue(strat.status == BollingerBandwithStrategyState.Peaked)
        self.assertTrue(strat.check_open_condition(self._create_bar(0.65)))
        self.assertTrue(strat.status == BollingerBandwithStrategyState.Peaked)
        self.assertFalse(strat.check_close_condition(self._create_bar(0.60)))
        self.assertTrue(strat.check_close_condition(self._create_bar(0.20)))

    def test_multiple_buys(self):
        contract = Stock("UNIT")
        strat = BollingerBandwithStrategy(contract, 1000)
        strat.order_manager = self.trader.order_manager

        self.assertTrue(strat.status == BollingerBandwithStrategyState.Looking)
        bw = 0
        while not strat.check_open_condition(self._create_bar(bw)):
            bw += 0.1

        strat.open_position(self._create_bar(bw))
        # now simulate the position filling
        # now simulate the position profiting

        bw = 0
        while not strat.check_open_condition(self._create_bar(bw)):
            bw += 0.1

        strat.open_position(self._create_bar(bw))




    

    # def test_order(self):
    #     contract = Stock("UNIT")
    #     strat = BollingerBandwithStrategy(contract, 1000)
    #     strat.run(self.trader)
    #     strat.open_position(self._create_bar(0.25))
    #     self.assertTrue(strat.order_placed)

if "__main__" == __name__:
    unittest.main()
