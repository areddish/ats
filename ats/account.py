from ibapi.contract import Contract


class Account:
    def __init__(self, name):
        self.account_name = ""
        self.values = {}
        self.positions = {}
        self.updating = False

    def balance(self):
        return self.values.get("EquityWithLoanValue",0)

    def update_account_value(self, key: str, val: str, currency: str):
        self.updating = True
        self.values[key] = (val, currency)


    def update_portfolio(self, contract: Contract, position: float,
                        marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float,
                        realizedPNL: float):
        self.updating = True
        self.positions[contract.symbol] = (
            position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL)

    def account_download_end(self):
        self.updating = False

#######
## Stores information about the IB Account
#######
class AccountManager(object):
    def __init__(self):
        self.accounts = {}

    def add_account(self, account_name):
        assert account_name not in self.accounts
        self.accounts[account_name] = Account(account_name)

    def update_account_value(self, key: str, val: str, currency: str, accountName: str):
        self.accounts[accountName].update_account_value(key, val, currency)

    def account_download_end(self, accountName: str):
        self.accounts[accountName].account_download_end()

    def update_portfolio(self, contract: Contract, position: float,
                        marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float,
                        realizedPNL: float, accountName: str):
        self.accounts[accountName].update_portfolio(contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL)

    def get_total_balance(self):
        total = 0
        for account_name in self.accounts:
            total += self.accounts[account_name].balance()
        return total