from .barutils import BarAggregator, BarData
from .requests import RealTimeBarSubscription

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, DateTime

import datetime

# TODO: Duration in seconds? or enum?

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

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
        self.bar_db.record_bar(contract, bar)

        agg = self.aggregators[contract.symbol]

        agg.add_bar(bar)
        # local_time = time.localtime(timeStamp)
        # pretty_print_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
        # print(reqId, pretty_print_time, high, low, open, close,
        #       volume, count)

    def on_historical_bar(self, contract, bar):
        b = BarData()
        b.time = datetime.datetime.fromtimestamp(int(bar.date))
        b.open = bar.open
        b.high = bar.high
        b.low = bar.low
        b.close = bar.close
        b.volume = bar.volume
        b.average = bar.average
        b.barCount = bar.barCount
        self.bar_db.record_bar(contract, b)

    def subscribe(self, contract, duration="1 min", callback=None):
        self.aggregators[contract.symbol] = BarAggregator(contract, "c:\\temp", callback=callback)

        request = RealTimeBarSubscription(contract, self)

        assert contract.symbol not in self.subscriptionRequests
        self.subscriptionRequests[contract.symbol] = request

        self.broker.handle_request(request)

    def subscribe_from(self, contract, duration="1 min", start=None, callback=None):
        ''' Subscribe from a date before and then continuing
        '''
        pass

    def unsubscribe(self, contract):
        # Remove/Flush self.aggregators[contract.symbol]

        request = self.subscriptionRequests[contract.symbol]
        self.broker.cancel_request(request)