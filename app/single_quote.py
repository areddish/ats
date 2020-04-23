from ats.ats import BrokerPlatform
from ats.assets import Stock, Future
from ats.requests import SnapshotQuote, ContractDetailsRequest
from datetime import datetime
from ats.asset_utils import findNearestContractMonth
from ats.barmanager import BarManager

if "__main__" == __name__:
    print("Starting up...")

    trader = BrokerPlatform(7496, "1010")
    try:
        trader.connect()

        if (not trader.is_connected):
            print ("Couldn't connect.")
            exit(-1)

        request = SnapshotQuote(Stock("MSFT"))
        #trader.handle_request(request)

        print(f"Ask Price {request.ask}")
        print(f"Last Price {request.last}")
        print(f"Bid Price {request.bid}")
        print(f"Volume {request.volume}")

        next_future  = findNearestContractMonth(trader, Future("ES"))
        
        print ("Getting quote: ",next_future.symbol,next_future.lastTradeDateOrContractMonth)
        request = SnapshotQuote(next_future)
        trader.handle_request(request)
        print(f"Ask Price {request.ask}")
        print(f"Last Price {request.last}")
        print(f"Bid Price {request.bid}")
        print(f"Volume {request.volume}")

        def p(bar, bars):
            print(bar)
            print(bars)

        bm = BarManager(None, None)
        bm.connect_broker(trader)
        #bm.subscribe(next_future, callback=p)
        bm.subscribe(next_future, period=24, callback=p)
        trader.run()

        print("Shutting down...")
        trader.disconnect()
    except KeyboardInterrupt:
        print("Interrupt! Closing...")
        trader.disconnect()

