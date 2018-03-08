from threading import Event


class RequestManager():
    def __init__(self):
        self.available_request_ids = list(range(1, 101))
        self.available_single_use_ids = list(range(2000, 2100))
        self.requests = {}

    def create_sync_request(self):
        id = self.get_next_free_id(True)
        e = Event()
        # check we don't have a request already
        self.requests[id] = e
        return id, e

    def mark_finished(self, reqId):
        self.requests[reqId].set()
        self.free_request(reqId)

    def get_next_free_id(self, single_use=False):
        if (single_use):
            return self.available_single_use_ids.pop()
        return self.available_request_ids.pop()

    def free_request(self, id):
        # check if we have something
        existing_event = self.requests[id]
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
