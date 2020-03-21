from enum import Enum
from .request import Request, DummyRequest

# Debugging is easier if we have a set range for each type of calls. Each category gets 100 calls alloted to it. 
# Order ID's are separate.
class RequestType(Enum):
    HISTORICAL = 1
    CONTRACT_DETAILS = 2
    ORDERS = 3
    DIVIDEND_DETAILS = 4

class RequestManager():
    def __init__(self):
        self.available_request_ids = list(range(1, 101))
        self.available_single_use_ids = list(range(2000, 2100))
        self.freed_request_ids = []
        self.freed_single_use_ids = []
        self.requests = {}

    def add(self, request: Request):
        id = self.__get_next_free_id(request.request_type, request.is_synchronous)
        request.request_id = id
        self.requests[id] = request
        print(self.__class__,"Adding request:", id, type(request))

    def get(self, request_id):
        #print (self.__class__,"Getting:", request_id, request_id in self.requests)
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
        request.event.set()
        #del self.requests[reqId]
        self.__free_request(reqId)

    def __get_next_free_id(self, request_category, single_use=False):
        
        if (single_use):
            freed = self.freed_single_use_ids
            available = self.available_single_use_ids
        else:
            freed = self.freed_request_ids
            available = self.available_request_ids

        if not available:
            assert len(freed) > 0
            # Reclaim some freed ids
            for i in range(0, max(5, len(freed))):
                req_id = freed.pop(0)
                del self.requests[req_id]
                available.append(req_id)

        return available.pop()

    def __free_request(self, id):
        # check if even is in weird state
        if id >= 2000:
            print(f"freeing single... {id}")
            self.freed_single_use_ids.append(id)
        else:
            print(f"freeing request... {id}")
            self.freed_request_ids.append(id)
