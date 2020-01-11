

# reqId = 30


# some_fun(reqId,. ..):
# 	blocking_req_ids[reqId] = event()
# 	# make call
# 	blocking_req_ids[reqId].wait()

# some_fun_callback():
# 	# process

# some_fun_callback_with_end():
# 	# process
# 	e = blocking_Req_ids[reqid]
# 	blocking_Req_ids[reqid].remove()
# 	e.set/signal()
	

class Request:
    def __init__(self, reqId, request_start_fn, request_end_fn, *kwargs):
        self.reqId = reqId
        self.event = Event()
        self.request = request_start_fn
        self.complete = request_end_fn
        self.args = kwargs

    def issue(self):
        self.request(self.reqId, *kwargs)

class RequestManager:
    def __init__(self):
        self.pendingRequests = {}
    
    def record_start_of_request(self, reqId):
        if (self.pendingRequests[reqId] != None):
            raise ValueError

        self.pendingRequests[reqId] = RequestResponse(reqId)

    def complete_request(self, reqId)
        pass

class RequestResponse:
    def __init__(self, reqId):