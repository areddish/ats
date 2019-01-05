class HistoricalDataProvider:
    def __init__(self, broker):
        self.broker = broker
        self.broker.register_historical_data_provider(self)
    
    def get_earliest_timestamp(contract, data_type):



data = HistoricalDataProvider(broker)
ts = data.get_earliest_timestamp(Stock("MSFT"), "TRADES")
data.get_bar_data(Stock("MSFT"), ts, "1 M", )
