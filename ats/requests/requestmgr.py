from enum import Enum
from .request import Request

# Debugging is easier if we have a set range for each type of calls. Each category gets 100 calls alloted to it. 
# Order ID's are separate.
class RequestType(Enum):
    HISTORICAL = 1
    CONTRACT_DETAILS = 2
    ORDERS = 3

class RequestManager():
    def __init__(self):
        self.available_request_ids = list(range(1, 101))
        self.available_single_use_ids = list(range(2000, 2100))
        self.requests = {}

    def add(self, request: Request):        
        id = self.__get_next_free_id(request.request_type, request.is_synchronous)
        request.request_id = id
        self.requests[id] = request
        print(self.__class__,"Adding request:", id, type(request))

    def get(self, request_id):
        print (self.__class__,"Getting:", request_id)
        return self.requests[request_id]

    # def remove(self, request: Request):
    #     request_id = request.request_id
    #     del self.requests[request_id]
    #     self.__free_request(request_id)

    # def create_sync_request(self):
    #     id = self.get_next_free_id(True)
    #     e = Event()
    #     # check we don't have a request already
    #     self.requests[id] = e
    #     return id, e

    def mark_finished(self, reqId, **kwargs):
        request = self.requests[reqId]        
        request.complete(**kwargs)
        del self.requests[reqId]
        self.__free_request(reqId)

    def __get_next_free_id(self, request_category, single_use=False):
        
        if (single_use):
            return self.available_single_use_ids.pop()
        return self.available_request_ids.pop()

    def __free_request(self, id):
        # check if even is in weird state
        self.requests[id] = None
        if id <= 2000:
            self.available_single_use_ids.append(id)
        else:
            self.available_request_ids.append(id)

# class RequestSynchronizer:
#     def __init__(self, reqId):
#         self.event = Event()

#     def start():
#         pass

#     def end():
#         self.event.set()