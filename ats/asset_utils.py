from datetime import datetime
from .requests import ContractDetailsRequest
from .assets import Future

def findNearestContractMonth(platform, contract):
    assert platform
    assert contract

    # Set the last trade to this year
    contract.lastTradeDateOrContractMonth = datetime.now().year
      
    # Get contract details for this year
    request = ContractDetailsRequest(contract)
    platform.handle_request(request)

    # now find the one nearest to today.
    now = datetime.now()
    distance = 365
    nearest_details = None
    for detail in request.details:
        dt = datetime.strptime(detail.contractMonth, "%Y%m")
        if (now < dt):
            delta = dt - now
            if delta.days < distance:
                distance = delta.days
                nearest_details = detail
        
    return nearest_details.contract, nearest_details