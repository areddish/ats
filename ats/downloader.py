import datetime
from datetime import datetime, timedelta
from threading import Thread

"""
The maximum number of simultaneous open historical data requests from the API is 50. In practice, it will probably be more efficient to have a much smaller number of requests pending at a time.
Pacing Violations for Small Bars (30 secs or less)
Although Interactive Brokers offers our clients high quality market data, IB is not a specialised market data provider and as such it is forced to put in place restrictions to limit traffic which is not directly associated to trading. A Pacing Violation1 occurs whenever one or more of the following restrictions is not observed:
Making identical historical data requests within 15 seconds.
Making six or more historical data requests for the same Contract, Exchange and Tick Type within two seconds.
Making more than 60 requests within any ten minute period.
Note that when BID_ASK historical data is requested, each request is counted twice. In a nutshell, the information above can simply be put as "do not request too much data too quick".
Important: the above limitations apply to all our clients and it is not possible to overcome them. If your trading strategy's market data requirements are not met by our market data services please consider contacting a specialised provider.
"""
class ContractInfo:
    def __init__(self, reqId, contract)
        self.reqId = reqId
        self.symbol = contract
        self.bars = []

    def onBar(self):
        self.bars.append(b)

class Downloader:
    def __init__(self, trader, path = None):
        self.trader = trader
        self.request_mapping = {}
        now = datetime.now()
        nearest_close_offset = timedelta(day = -1 if now.hour < 16 else 0)
        self.start = datetime(now.year, now.month, now.day, 4, 0) + nearest_close_offset
        self.requst_window = timedelta(days = -2)
    def start_request(self, reqId, contract):
        self.request_mapping[reqId] = ContractInfo(reqId, contract)

    def onData(self,bar):


    def onDataFinished(self, reqId):
        # Write out files
        # Request next chunk
print ("starting at: ",start)
while (start.year > 2017): #1980):
    print ("requested from ", start, "to", start+walk_back)
    # request start, start+walk_back
    print ("folder is", "{}\\{}\\{}-{}-1-min.csv".format(start.year, start.month, start.hour, start.minute))
    trader.reqHistoricalData(id, contract, end, "2 D", "1 min", "TRADES", 1, 2, [])
    start += walk_back
    #(10)

# Each day is 1 minute * 6.5 hrs = 60 * 6.5 = 390 entries max.

# ask for 1 day every 10 seconds = 6 days a minute or 360 days an hour
