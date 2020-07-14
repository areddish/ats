from ats.strategies.strategy import Strategy
from ats.barmanager import BarManager, BarDb
from ats.bollingerbands import bbands_last, bbands_percent
from ats.util.util import get_user_file
from enum import Enum
from ats.sms.twilio import send_notification

def snap_to_increment(price, min_tick):
    return min_tick * (price + min_tick) // min_tick

class BollingerBandwithStrategyState(Enum):
    Looking = 1
    Peaked = 2
    Dipped = 3

class Indicators(Enum):
    BollingerBands = 1

class Indicator():
    def __init__(self, owner, contract, type):
        self.owner = owner
        self.contract = contract
        self.type = type

    def on_bar(self, current_bar, all_bars):
        self.owner.on_bar(current_bar)

class BollingerBandIndicator(Indicator):
    def __init__(self, owner, contract, period, n_std_dev=2):
        super().__init__(owner, contract, Indicators.BollingerBands)
        self.period = period
        self.num_std_dev = n_std_dev
        send_notification("Starting...")

    def on_bar(self, current_bar, all_bars):
        print("BollingerBandIndicator: got bar... ",end="")
        # need to have a minimum of period bars
        if len(all_bars) < self.period:
            print(f"Not enough data {len(all_bars)}/{self.period}, skipping")
            return

        # data = [bar.close for bar in all_bars]
        # upper, middle, lower = bbands_last(data, window_size=self.period, num_std_dev=self.num_std_dev)
        # percent = bbands_percent(upper, lower, current_bar.close)
        relevant_bars = all_bars.iloc[-self.period:].copy()

        col_name = f"bb_{self.period}"
        relevant_bars[col_name] = relevant_bars["close"].rolling(window=self.period).mean()
        relevant_bars[col_name+"_std"] = relevant_bars["close"].rolling(window=self.period).std()
        relevant_bars.dropna(inplace=True)        
        relevant_bars[col_name+"_upper"] = relevant_bars[col_name] + self.num_std_dev * relevant_bars[col_name+"_std"]
        relevant_bars[col_name+"_lower"] = relevant_bars[col_name] - self.num_std_dev * relevant_bars[col_name+"_std"]
        relevant_bars[col_name+"_pct"] = (current_bar.iloc[0]["close"] - relevant_bars[col_name+"_lower"])/(relevant_bars[col_name+"_upper"]-relevant_bars[col_name+"_lower"])
        relevant_bars.dropna(inplace=True)    

        augmented_bar = dict(relevant_bars.tail(1).iloc[0])
        augmented_bar["indicators"] = {
                self.type: {
                    self.period: {
                        "upper": augmented_bar[col_name+"_upper"],
                        "middle": augmented_bar[col_name],
                        "lower": augmented_bar[col_name+"_lower"],
                        "percent": augmented_bar[col_name+"_pct"]
                    }
                }
            }
        print(f"Computed: {augmented_bar}. Calling strategy")
        super().on_bar(augmented_bar, all_bars)

def create_indicator(strategy, contract, indicator_data):
    if indicator_data["type"] == Indicators.BollingerBands:
        return BollingerBandIndicator(strategy, contract, indicator_data["period"], 2)

class InidicatorStrategy(Strategy):
    def __init__(self, contract, allocation):
        super().__init__(allocation)
        self.contract = contract
        self.bar_manager = None
        self.indicator = None
        self.registered = False

    def register(self, trader):
        assert not self.bar_manager
        # TODO: fix this bar db
        self.bar_manager = BarManager(trader, None)#BarDb(get_user_file(trader.APP_NAME, f"{self.contract.symbol}-{self.contract.lastTradeDateOrContractMonth}.db")))

        if self.indicator and not self.registered:
            self.bar_manager.subscribe(self.indicator.contract, period=24, callback=self.indicator.on_bar)
            self.registered = True

    def unregister(self, trader):
        if self.registered:
            self.bar_manager.unsubscribe(self.indicator.contract)

class BollingerBandwithStrategy(InidicatorStrategy):
    def __init__(self, contract, allocation, min_tick=0.01, bottom_threshold=0.2, top_threshold=0.7, period=24):
        super().__init__(contract, allocation)
        self.status = BollingerBandwithStrategyState.Looking

        self.has_dipped = False
        self.bottom_threshold = bottom_threshold
        self.top_threshold = top_threshold
        self.qty_desired = 0
        self.qty_owned = 0
        self.order_placed = False
        # needed?
        self.indicator_name = f"BBANDWIDTH_{period}"
        # peroid minute bollinger bands
        self.indicator = create_indicator(self, self.contract, { "type": Indicators.BollingerBands, "period": period })
        self.min_tick = min_tick

    def check_open_condition(self, augmented_bar):
        """
            The buy condition for this strategy is satisfied by two conditions:

                1. The price must have first dipped below the bottom_threshold
                2. The price must then have broken above the bottom_threshold

        """
        # Check if we have dipped or peaked
        bband_percent = augmented_bar["indicators"][Indicators.BollingerBands][24]["percent"]

        if self.status == BollingerBandwithStrategyState.Looking:
            if bband_percent < self.bottom_threshold:
                self.status = BollingerBandwithStrategyState.Dipped
            elif bband_percent > self.top_threshold:
                self.status = BollingerBandwithStrategyState.Peaked
            return False

        elif self.status == BollingerBandwithStrategyState.Dipped:
            # We want to buy when, after having dipped, we cross back above the threshold
            return bband_percent >= self.bottom_threshold

        elif self.status == BollingerBandwithStrategyState.Peaked:            
            return bband_percent <= self.top_threshold

    def check_close_condition(self, augmented_bar):
        """
            The sell condtiion is that we have a bar that is at or above the top_threshold

            TODO: In the future we want to eliminate this check and allow the order to 
            float up.
        """
        # Check if we have dipped or peaked
        bband_percent = augmented_bar["indicators"][Indicators.BollingerBands][24]["percent"]

        assert self.status != BollingerBandwithStrategyState.Looking
        
        if self.status == BollingerBandwithStrategyState.Dipped:
            # We want to sell when we hit the top threshold
            return bband_percent >= self.top_threshold
        elif self.status == BollingerBandwithStrategyState.Peaked:            
            return bband_percent <= self.bottom_threshold


    def on_tick(self, tick):
        """
            TODO: Put logic here to raise the stop as the price moves up.
        """
        pass

    def on_fill(self, qty):
        self.position = qty > 0

        # We can get out of order events here, so if we always want
        # the largest of the messages.
        self.qty_owned = max(self.qty_owned, qty)
        if self.qty_desired == self.qty_owned:
            # Mark order filled
            self.order_placed = False

    def on_cancel(self):
        self.order_placed = False

        # We received this after a partial/full fill. Ignore
        if self.qty_owned > 0:
            print(f"on_cancel after fill of {self.qty_owned}/{self.qty_desired}")
            pass

    def on_end_of_day(self):
        if self.order_placed:
            # TODO: cancel order
            pass

        if self.position and self.day_position:
            self.close_position()

    def open_position(self, augmented_bar):
        top_of_band = augmented_bar["indicators"][Indicators.BollingerBands][24]["upper"]
        bottom_of_band = augmented_bar["indicators"][Indicators.BollingerBands][24]["lower"]

        # TODO: this should compute based on self.allocation / price + fees
        self.qty_desired = 1

        if self.status == BollingerBandwithStrategyState.Dipped:              
            # Take profit at the upper threshold
            profit = ((top_of_band - bottom_of_band) * self.top_threshold) + bottom_of_band
            # Stop is if we break down below band.
            stop = bottom_of_band

            """
            TODO: We should have a check for a minimum amount of profit and stop and make sure:
                1. They aren't really close i.e. they should be X tick sizes away
                2. That profit generates a profit worth taking the risk for
                3. That stop isn't huge, consider a minimum $, % or other check along with computing it
            """

            market_order, profit_order, stop_order = self.order_manager.create_bracket_order(self.contract, self.qty_desired, snap_to_increment(profit, self.min_tick), snap_to_increment(stop, self.min_tick))
        elif self.status == BollingerBandwithStrategyState.Peaked:
            # Take profit at the bottom threshold
            profit = ((top_of_band - bottom_of_band) * self.top_threshold) + bottom_of_band
            # Stop is if we break down below band.
            stop = bottom_of_band

            """
            TODO: We should have a check for a minimum amount of profit and stop and make sure:
                1. They aren't really close i.e. they should be X tick sizes away
                2. That profit generates a profit worth taking the risk for
                3. That stop isn't huge, consider a minimum $, % or other check along with computing it
            """

            market_order, profit_order, stop_order = self.order_manager.create_bracket_order(self.contract, self.qty_desired, snap_to_increment(profit, self.min_tick), snap_to_increment(stop, self.min_tick))

        market_order.on_filled = self.positionFill
        profit_order.on_filled = self.positionClosed
        stop_order.on_filled = self.positionStoppedOut

        self.order_manager.place_order(market_order)
        self.order_manager.place_order(profit_order)
        self.order_manager.place_order(stop_order)
        self.order_placed = True
        send_notification(f"{self.status}: Sending orders market, {profit} {stop}...")

    def close_position(self, augmented_bar):
        # TODO: Right now we are using bracket orders to close. So this isn't
        # needed to do anything.
        pass        
        
    def positionFill(self, avg_price):
        self.position = True
        self.has_dipped = False
        send_notification(f"OPEN POSITION: {self.contract.symbol} {avg_price}...")

    def positionStoppedOut(self, avg_price):
        self.position = False
        self.has_dipped = True
        send_notification(f"STOP POSITION: {self.contract.symbol} {avg_price}...")
        self.order_placed = False

    def positionClosed(self, avg_price):
        self.position = False
        self.has_dipped = False
        send_notification(f"CLOSE POSITION: {self.contract.symbol} {avg_price}...")
        self.order_placed = False