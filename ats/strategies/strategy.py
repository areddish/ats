## Primary drivers
## on_bar: receives a real time bar
## on_fill: receives a notification that the order has filled so that the strategy can manage position
## on_cancel: receives a notification that the order has been cancelled
## on_end_of_day: receives a notification that the trading day is about to end. 


class Strategy:
    def __init__(self, allocation):
        self.bank = allocation

        # TODO: This should look into our own record keeping as well as account positions
        self.position = False

        # TODO: Rethink for Futures or continuously traded contracts.
        # This position is only held for the day, we should close if no trigger by end of day.
        self.day_position = True

    def on_tick(self, tick):
        pass

    def on_bar(self, augmented_bar):
        # Compute indicators
        augmented_bar = self.compute_indicators(augmented_bar)

        # Make buy / sell decision
        if (self.position):
            if self.check_sell_condition(bar):
                self.open_position(augmented_bar)
        else:
            if self.check_buy_condition(bar):
                self.close_position(augmented_bar)

    def on_fill(self, qty):
        raise NotImplementedError()

    def on_cancel(self):
        raise NotImplementedError()

    def on_end_of_day(self):
        if self.position and self.day_position:
            self.close_position()

    def check_buy_condition(self, augmented_bar):
        assert not self.position
        return False

    def check_sell_condition(self, augmented_bar):
        assert self.position
        return False

    def open_position(self):
        raise NotImplementedError()

    def close_position(self):
        raise NotImplementedError()

    def register(self):
        raise NotImplementedError()

    def unregister(self):
        raise NotImplementedError()

    def run(self, trader):
        self.register()
        """
        TODO:
            Need a way to unregister before disconnect?
            Need a way to reconect if connection lost? or is that handled for us?
            Need a way to know that we've lost data?
            Need a way to re-sync our state vs real state in the event of disconnect, etc
        """
        trader.run()

        # TODO: This should be done before it ges here... we've already disconnected
        # self.unregister()