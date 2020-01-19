from ats.orders import create_bracket_order

class BollingerBandwithStrategy(Strategy):
    def __init__(self, contract, allocation, bottom_threshold=0.2, top_threshold=0.7):
        super().__init__(allocation)

        self.contract = contract
        self.has_dipped = False
        self.bottom_threshold = bottom_threshold
        self.top_threshold = top_threshold
        self.qty_desired = 0
        self.qty_owned = 0
        self.order_placed = False
        # needed?
        self.indicator_name = "BBANDWIDTH_24"

    def check_buy_condition(self, augmented_bar):
        """
            The buy condition for this strategy is satisfied by two conditions:

                1. The price must have first dipped below the bottom_threshold
                2. The price must then have broken above the bottom_threshold

        """
        # Check if we have dipped below
        self.has_dipped = self.has_dipped or augmented_bar.inidcators[indicator_name] < self.bottom_threshold 

        # We want to buy when, after having dipped, we cross back above the threshold
        return not self.order_placed and
               self.has_dipped and 
               augmented_bar.inidcators[indicator_name] >= self.bottom_threshold:

    def check_sell_condition(self, augmented_bar):
        """
            The sell condtiion is that we have a bar that is at or above the top_threshold

            TODO: In the future we want to eliminate this check and allow the order to 
            float up.
        """
        return augmented_bar.inidcators[indicator_name] >= self.top_threshold

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
        top_of_band = 0 # TODO:
        bottom_of_band = 0 # TODO:

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

        self.order = create_bracket_order(self.qty_desired, profit, stop)
        # TODO: place order
        self.order_placed = true

    def close_position(self, augmented_bar):
        # TODO: Right now we are using bracket orders to close. So this isn't
        # needed to do anything.