from ats.ats import BrokerPlatform
from ats.assets import Stock
from ats.requests import SnapshotQuote

if "__main__" == __name__:
    print("Starting up...")

    trader = BrokerPlatform(7496, "100")
    try:
        trader.connect()

        if (not trader.is_connected):
            print ("Couldn't connect.")
            exit(-1)

        request = SnapshotQuote(Stock("MSFT"))
        trader.handle_request(request)

        print(f"Ask Price {request.ask}")
        print(f"Last Price {request.last}")
        print(f"Bid Price {request.bid}")
        print(f"Volumne {request.volume}")

        print("Shutting down...")
        trader.disconnect()
    except KeyboardInterrupt:
        print("Interrupt! Closing...")
        trader.disconnect()

