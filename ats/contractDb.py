from ibapi.contract import ContractDetails

# backing-file, in the future cold be pulled from db / cloud storage
contract_db_file = "contract-info.json"

class ContractDb:
    def __init__(self):
        self.contracts = {}
        pass

    def load(self):
        with open(contract_db_file, "rb") as data_file:
            pass
        pass

    def update_contract(self, contract_details):
        self.contracts[contract_details.summary.symbol] = contract_details

    
    def save(self):
        with open(contract_db_file, "wb") as data_file:
            pass
        pass

