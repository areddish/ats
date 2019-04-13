class BollingerBandwithStrategy(Strategy):
    def __init__(self):
        self.has_dipped = False
        self.bottom_threshold = 0.2
        self.top_threshold = 0.7
        self.indicator_name = "BBANDWIDTH_24"

    def check_buy_condition(self, augmented_bar):
        self.has_dipped = self.has_dipped or  augmented_bar.inidcators[indicator_name] < self.bottom_threshold 
        return self.has_dipped and augmented_bar.inidcators[indicator_name] >= self.bottom_threshold:
            
    def buy_triggered(self):
        self.has_dipped = False

    def check_sell_condition(self, augmented_bar):
        return augmented_bar.inidcators[indicator_name] > self.top_threshold

    def sell_triggered(self):
        pass
