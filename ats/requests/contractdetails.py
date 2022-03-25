from .requestmgr import RequestType
from .request import Request

class ContractDetailsRequest(Request):
    def __init__(self, contract):
        super().__init__(contract, True)
        self.request_type = RequestType.CONTRACT_DETAILS
        self.details = {}


    def on_data(self, **kwargs):
        print(kwargs)
        self.details = kwargs["contractDetails"]
        