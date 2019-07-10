from .requestmgr import RequestType
from .request import Request

class OptionChainRequest(Request):
    def __init__(self, contract):
        super().__init__(contract, True)
        self.request_type = RequestType.CONTRACT_DETAILS
        self.strikes = {}

    def on_data(self, **kwargs):
        contractDetails = kwargs["contractDetails"]
        print("Recieved:", contractDetails.contract.localSymbol)
        self.strikes[contractDetails.contract.strike] = contractDetails.contract
