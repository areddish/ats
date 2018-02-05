from ibapi.contract import *

# These symbols require an exchange to be set otherwise we get an error since there
# are duplicates in the IB system. These are empirically found by getting an error
# when requesting a quote.
# https://pennies.interactivebrokers.com/cstools/contract_info/v3.9/index.php can be
# used to look up a symbol and if it has multiple stocks listed with the same name
# and different exchanges we need to specify an exchange.
# Also see: http://interactivebrokers.github.io/tws-api/basic_contracts.html#gsc.tab=0
tickers_that_need_primary_exchange = {
    "MSFT": "NASDAQ",
    "CSCO": "NASDAQ",
    "INTC": "NASDAQ"
}


class Stock(Contract):
    def __init__(self, symbol):
        self.symbol = symbol
        self.secType = "STK"
        if symbol in tickers_that_need_primary_exchange:
            self.primaryExchange = tickers_that_need_primary_exchange[symbol]
