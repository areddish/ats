from ibapi.common import BarData
from .barutils import barDataToDataFrame


class HistoricalDataMixin:
    def historicalData(self, reqId: int, bar: BarData):
        """ returns the requested historical data bars

        reqId - the request's identifier
        date  - the bar's date and time (either as a yyyymmss hh:mm:ssformatted
             string or as system time according to the request)
        open  - the bar's open point
        high  - the bar's high point
        low   - the bar's low point
        close - the bar's closing point
        volume - the bar's traded volume if available
        count - the number of trades during the bar's timespan (only available
            for TRADES).
        WAP -   the bar's Weighted Average Price
        hasGaps  -indicates if the data has gaps or not. """
        self.processHistoricalBar(reqId, bar)

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        """returns updates in real time when keepUpToDate is set to True"""
        self.processHistoricalBar(reqId, bar, is_update=True)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        """ Marks the ending of the historical bars reception. """
        args = locals().copy()
        del args["self"]
        del args["reqId"]
        self.request_manager.mark_finished(reqId, **args)

    def processHistoricalBar(self, reqId, barData, is_update=False):
        request = self.request_manager.get(reqId)
        df = barDataToDataFrame(barData)
        # if self.bar_manager:
        #    self.bar_manager.on_historical_bar(request.contract, df, is_update=is_update)
        request.on_data(reqId, df)
