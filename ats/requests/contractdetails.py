from .requestmgr import RequestType
from .request import Request

class ContractDetailsRequest(Request):
    def __init__(self, contract):
        super().__init__(contract, True)
        self.request_type = RequestType.CONTRACT_DETAILS

    def on_data(self, **kwargs):
        contractDetails = kwargs["contractDetails"]        
        print(contractDetails.contract.symbol,
              contractDetails.contractMonth, contractDetails.contract.conId, contractDetails)
        
        print(contractDetails.marketName)
        print(contractDetails.validExchanges)
        print(contractDetails.priceMagnifier)
        print(contractDetails.longName)
        print(contractDetails.industry)
        print(contractDetails.subcategory)
        print(contractDetails.tradingHours)
        print(contractDetails.liquidHours)
        print(contractDetails.contract)        
        
        #pickle.dump(contractDetails, open(contractDetails.contract.symbol, "wt"))