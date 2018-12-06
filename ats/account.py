from ibapi.contract import Contract

#######
## Stores information about the IB Account
#######
class AccountManager(object):
    def __init__(self):
        self.account_name = None
        self.account_balance = 0
        self.values = {}
        self.positions = {}
        self.updating = False

    def updateAccountValue(self, key: str, val: str, currency: str,
                           accountName: str):
        self.updating = True
        self.values[key] = (val, currency)
        print(f"${accoutnName}: ${key} = ${value} ${currency}"")

    def accountDownloadEnd(self, accountName: str):
        self.account_name = accountName
        self.updating = False

    def updatePortfolio(self, contract: Contract, position: float,
                        marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float,
                        realizedPNL: float, accountName: str):
        self.updating = True
        self.positions[contract.symbol] = (
            position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL)
