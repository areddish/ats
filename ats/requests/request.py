from threading import Event

class Request(object):
    def __init__(self, contract, is_synchronous=True):
        self.request_id = None
        self.is_synchronous = is_synchronous
        self.event = Event() if self.is_synchronous else None
        self.contract = contract
        self.request_type = None

    def on_data(self, **kwargs):
        pass

    def complete(self, **kwargs):
        if (self.is_synchronous):
            self.event.set()

    def on_error(self, error_code, errorString):
        # We didn't handle it, outer error handler should process.
        return False 