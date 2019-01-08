# Historical Data Download utility
#
# Given a date range and a symbol it will collect data about that symbol
import argparse
import datetime
import time
import threading
import os
from ats.ats import BrokerPlatform
from ats.assets import Stock, Future
from ats.requests import HistoricalDataRequest

MAX_VIX_FUTURES_MONTHS = 9

def to_ib_timestr(dt):
    return dt.strftime("%Y%m%d %H:%M:%S")


def to_duration(dt_start, dt_end):
    return f"{(dt_end - dt_start).seconds} S"

def get_vix_futures_data():
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    i = 0
    requests = []
    while i < MAX_VIX_FUTURES_MONTHS:
        date = datetime.datetime(year, month, 1)
        print(f"Getting VX{str(i)}: {date.strftime('%Y%m')}")

        # TODO: Create delayed data request
        VX = Future("VIX", exchange="CFE")
        VX.lastTradeDateOrContractMonth = f"{date.strftime('%Y%m')}"

        request = HistoricalDataRequest(VX, datetime.datetime.now(), "20 D", "1 day")
        request.set_data_folder("C:\\temp\\VX")
        requests.append(request)
        # Get the next month. If we roll over, then move to next year.
        month += 1
        if (month > 12):
            year += 1
            month = 1

        i += 1

    return requests

if "__main__" == __name__:
    try:
        broker = BrokerPlatform(7496, 110505, use_pace_api=True)        
        broker.connect()

        # Vix futures
        for req in get_vix_futures_data():
            broker.handle_request(req)

    except KeyboardInterrupt:
        print("Interrupt! Closing...")

    print("Done!")
    broker.disconnect()

