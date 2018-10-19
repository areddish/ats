## Primary drivers
## on_bar: receives a real time bar
## on_fill: receives a notification that the order has filled so that the strategy can manage position
## on_cancel: receives a notification that the order has been cancelled
## on_end_of_day: receives a notification that the trading day is about to end. 

class Strategy:
    def on_tick():
        pass

    def on_bar(Bar bar):
        # Compute indicators
        # make buy / sell decision
        
        pass

    