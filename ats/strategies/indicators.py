from ats.barmanager import BarManager, BarDb
from ats.sms.twilio import send_notification
from ats.strategies.strategy import Strategy

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

class RSIIndicator(Indicator):
    def __init__(self, owner, contract, period):
        super().__init__(owner, contract, Indicators.BollingerBands)
        self.period = period
        send_notification("Starting...")

    def on_bar(self, current_bar, all_bars):
        print("RSIIndicator: got bar... ",end="")
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

        rsi_val = 0
        augmented_bar = dict(relevant_bars.tail(1).iloc[0])
        augmented_bar["indicators"] = {
                self.type: {
                    self.period: {
                        "value": rsi_val,
                    }
                }
            }
        print(f"Computed: {augmented_bar}. Calling strategy")
        super().on_bar(augmented_bar, all_bars)
