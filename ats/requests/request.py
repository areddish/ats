from threading import Event

class Request(object):
    def __init__(self, contract, synchronus=True):
        self.requset_id = None
        self.is_synchronus = synchronus
        self.event = Event() if self.is_synchronus else None
        self.contract = None
        self.request_type = None

    def on_data(self, *args):
        pass

    def complete(self, *args):
        pass

    def on_error(self, error_code, errorString):
        # We didn't handle it, outer error handler should process.
        return False 