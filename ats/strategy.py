## Primary drivers
## on_bar: receives a real time bar
## on_fill: receives a notification that the order has filled so that the strategy can manage position
## on_cancel: receives a notification that the order has been cancelled
## on_end_of_day: receives a notification that the trading day is about to end. 


class Strategy:
    def __init__(self, allocation):
        self.bank = allocation
        self.position = False

    def on_tick(self, tick):
        if (self.position):
            self.on_price_move(tick)

    def on_bar(self, augmented_bar):
        # Compute indicators
        # make buy / sell decision
        
        if (self.position):
            sell = check_sell_condition(bar)
            if (sell):
                sell_position()
        else:
            buy = check_buy_condition(bar)
            if buy:
                buy()

    def check_buy_condition(self, augmented_bar):
        assert not self.position
        return False

    def check_sell_condition(self, augmented_bar):
        assert self.position
        return False

    
    