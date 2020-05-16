from .barutils import BarAggregator, BarData
from .requests import RealTimeBarSubscription, RealTimeBarSubscriptionWithBackFill, HistoricalDataRequest

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, DateTime

import datetime
from enum import Enum

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class BarDuration(Enum):
    FiveSeconds = 5
    OneMinute = 5 * 12
    FiveMinutes = OneMinute * 5
    FifeteenMinutes = FiveMinutes*3

class BarObj(Base):
    __tablename__ = "bars"

    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    open_price = Column(Float)
    close_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    volume = Column(Float)

class BarDb:
    def __init__(self, db_file):
        engine = create_engine('sqlite:///'+db_file)
        self.session = sessionmaker(bind=engine)()
        Base.metadata.create_all(engine)

    def record_bar(self, contract, bar):
        existing_bar = self.session.query(BarObj).filter(BarObj.start == bar.time).first()
        if not existing_bar:
            obj = BarObj(start = bar.time,
            open_price = bar.open,
            close_price = bar.close,
            high_price = bar.high,
            low_price = bar.low,
            volume = bar.volume)
            self.session.add(obj)
            self.session.commit()

    def get_bars(self, contract, start_date, end_date=None):
        pass



class BarManager(object):
    def __init__(self, broker, bardb):
        self.aggregators = {}
        self.subscriptionRequests = {}
        self.broker = broker
        self.bar_db = bardb

    def connect_broker(self, broker):
        self.broker = broker

    def on_bar(self, contract, bar):
        if self.bar_db:
            self.bar_db.record_bar(contract, bar)

        agg = self.aggregators.get(contract.symbol, None)
        if agg:
            agg.add_bar(bar)
            # local_time = time.localtime(timeStamp)
            # pretty_print_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
            # print(reqId, pretty_print_time, high, low, open, close,
            #       volume, count)

    def on_historical_bar(self, contract, bar, is_update=False):
        b = self.convert_bar(bar)
        if is_update:
            self.on_bar(contract, b)
        else:
            if self.bar_db:
                self.bar_db.record_bar(contract, b)

    def on_historical_finished(self, contract):
        ''' This should mark that we have no gaps in the data and are ready
            to send call backs as the bar agg should be primed with the requested
            data plus any new
        '''
        pass

    def subscribe(self, contract, duration=BarDuration.OneMinute, period=1, callback=None):
        if period > 1:
            callback = self.create_backfill_callback(contract, callback, period)
        self.aggregators[contract.symbol] = BarAggregator(contract, desiredTimeSpanInSeconds=duration, callback=callback)


        # Create the initial realtime query
        request = RealTimeBarSubscription(contract, self)

        assert contract.symbol not in self.subscriptionRequests
        self.subscriptionRequests[contract.symbol] = request

        self.broker.handle_request(request)

        # Create a historical request for last period - 1 bars.

    def subscribe_from(self, contract, duration=BarDuration.OneMinute, end_date=None, callback=None):
        ''' Subscribe from a date before and then continuing
        '''
        self.aggregators[contract.symbol] = BarAggregator(contract, desiredTimeSpanInSeconds=duration, callback=callback, live=False)

        # TODO: this should be contract passing in
        request = RealTimeBarSubscriptionWithBackFill(contract.symbol, end_date, self)
        assert contract.symbol not in self.subscriptionRequests
        self.subscriptionRequests[contract.symbol] = request

        self.broker.handle_request(request)

    def unsubscribe(self, contract):
        # Remove/Flush self.aggregators[contract.symbol]

        request = self.subscriptionRequests[contract.symbol]
        self.broker.cancel_request(request)

    def on_backfill_complete(self, contract, bars):
        self.aggregators[contract.symbol].on_backfill_complete(bars)

    def create_backfill_callback(self, contract, original_callback, period):
        def callback_to_trigger_backfill(bar, bars):
            def on_backfill_complete():
                # add all of the bars
                self.aggregators[contract.symbol].back_fill(bar, request.bars, original_callback)

            # We have 1 minute of data, lets get period - 1.
            end_date = bar.index + datetime.timedelta(seconds=5) - datetime.timedelta(minutes=1)
            request = HistoricalDataRequest(contract, end_date.to_pydatetime()[0], duration=f"{60*(period-1)} S")
            request.on_complete = on_backfill_complete
            self.broker.handle_request(request)

            # Disable current callback until we fill all of the backdated requests
            self.aggregators[contract.symbol].callback = None

        return callback_to_trigger_backfill

            
    def convert_bar(self, bar):
        b = BarData()
        b.time = datetime.datetime.fromtimestamp(int(bar))
        b.open = bar.open
        b.high = bar.high
        b.low = bar.low
        b.close = bar.close
        b.volume = bar.volume
        b.average = bar.average
        b.barCount = bar.barCount
        return b