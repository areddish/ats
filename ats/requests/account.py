class AccountSummaryRequest(object):
    def __init__(self):
        super().__init__(None, True)

    def on_data(self, **kwargs):
        pass

    def complete(self, **kwargs):
        if (self.is_synchronous):
            self.event.set()

    def on_error(self, error_code, errorString):
        # We didn't handle it, outer error handler should process.
        return False 