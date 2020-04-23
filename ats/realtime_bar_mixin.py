from .barutils import createBarDataFrame
from ibapi.common import TickerId

class RealTimeBarMixin:
    def realtimeBar(
        self,
        reqId: TickerId,
        time: int,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: int,
        wap: float,
        count: int,
    ):
        """ Updates the real time 5 seconds bars

        reqId - the request's identifier
        bar.time  - start of bar in unix (or 'epoch') time
        bar.endTime - for synthetic bars, the end time (requires TWS v964). Otherwise -1.
        bar.open  - the bar's open value
        bar.high  - the bar's high value
        bar.low   - the bar's low value
        bar.close - the bar's closing value
        bar.volume - the bar's traded volume if available
        bar.WAP   - the bar's Weighted Average Price
        bar.count - the number of trades during the bar's timespan (only available
            for TRADES)."""
        self.request_manager.get(reqId).on_data(
            **{
                "reqId": reqId,
                "dataFrame": createBarDataFrame(time, open, high, low, close, volume),
            }
        )
