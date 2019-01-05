from .barutils import BarAggregator
from .requests import RealTimeBarSubscription

# TODO: Duration in seconds? or enum?

class BarManager(object):
    def __init__(self, broker):
        self.aggregators = {}
        self.subscriptionRequests = {}
        self.broker = broker

    def on_bar(self, contract, bar):
        agg = self.aggregators[contract.symbol]

        agg.add_bar(bar)
        # local_time = time.localtime(timeStamp)
        # pretty_print_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
        # print(reqId, pretty_print_time, high, low, open, close,
        #       volume, count)

    def subscribe(self, contract, duration="1 min"):
        self.aggregators[contract.symbol] = BarAggregator(contract, "c:\\temp")

        request = RealTimeBarSubscription(contract, self)
        self.subscriptionRequests = request
        self.broker.handle_request(request)

    def unsubscribe(self, contract, duration="1 min"):
        # Remove/Flush self.aggregators[contract.symbol]

        request = self.subscriptionRequests[contract.symbol]
        self.broker.cancel_request(request)
        