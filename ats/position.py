# Submit order when the condition happens. I.e. price reaches a level we want to buy at. We 
# take the following steps:

#     BUY @ market
#     Attach child order for stop loss and profit
#     Profit order has a trailing trigger
    
#     Close / cancel at 3:50 if position play = daily

class Position:
    def __init__(self, contract):
        self.contract = contract
        self.size = qty
        self.value = ..
        should register for market update to keep it updated?

        self.hasPosition = false
        self.cash = 0
        self.position

    def on_tick():
        pass

    def close():
        pass

class Bank:
    def __init__(self, cash):
        self.cash = cash

    def has_cash(self):
        return self.cash > 0

    def withdraw(cash):
        self.cash -= cash

    def deposit(cash):
        self.cash += cash
