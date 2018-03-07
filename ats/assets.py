import datetime
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
    def __init__(self, symbol, primaryExchange=None, currency="USD"):
        super().__init__()
        self.symbol = symbol
        self.secType = "STK"
        self.exchange = "SMART"
        self.currency = currency
        if primaryExchange != None:
            self.primaryExchange = primaryExchange
        if symbol in tickers_that_need_primary_exchange:
            self.primaryExchange = tickers_that_need_primary_exchange[symbol]


class Index(Contract):
    def __init__(self, symbol, exchange="CBOE"):
        super().__init__()
        self.symbol = symbol
        self.secType = "IND"
        self.exchange = exchange


class Option(Contract):
    def __init__(self, underlying, expiry):
        super().__init__()
        self.symbol = underlying
        self.secType = "OPT"


class Future(Contract):
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
        self.secType = "FUT"
        self.currency = "USD"
        self.lastTradeDateOrContractMonth = "201803"
        self.primaryExchange = "GLOBEX"


class Forex(Contract):
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
        self.secType = "CASH"


SP500 = Index("SPX")
Dow = Index("DJI")
