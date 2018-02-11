from ats.assets import Stock
from ibapi.order import Order
from enum import Enum


class OrderType(Enum):
    BUY = 1
    SELL = 2


def create_market_order(quantity, action_type):
    order = Order()
    order.totalQuantity = quantity
    order.orderType = "MKT"
    if action_type == OrderType.BUY:
        order.action = "BUY"
    else:
        order.action = "SELL"


def create_limit_order(quantity, limit):
    order = Order()
    order.totalQuantity = quantity
    order.orderType = "MKT"
    # order.limit?