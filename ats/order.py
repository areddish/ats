from ibapi.contract import Contract
from ibapi.order import Order
from enum import Enum


class OrderType(Enum):
    BUY = 1
    SELL = 2


next_order_id = 1


def get_next_order_id():
    global next_order_id
    result = next_order_id
    next_order_id += 1
    return result


def create_order(qty, type):
    order = Order()
    order.orderId = get_next_order_id()
    order.totalQuantity = qty
    order.action = "BUY" if type == OrderType.BUY else "SELL"
    order.transmit = True
    return order


def create_market_order(qty, type):
    order = create_order(qty, type)
    order.orderType = "MKT"
    return order


def create_limit_order(qty, type, price):
    order = create_order(qty, type)
    order.orderType = "LMT"
    order.lmtPrice = price
    return order


def create_stop_order(qty, type, price):
    order = create_order(qty, type)
    order.orderType = "STP"
    order.auxPrice = price
    return order


def create_bracket_order(qty, type, profit_price, stop_loss_price):
    market_order = create_market_order(qty, OrderType.BUY)
    profit_taker_order = create_limit_order(qty, OrderType.SELL, profit_price)
    stop_loss_order = create_stop_order(qty, OrderType.SELL, stop_loss_price)

    market_order.transmit = False
    profit_taker_order.transmit = False

    profit_taker_order.parentId = market_order.orderId
    stop_loss_order.parentId = market_order.orderId

    return [market_order, profit_taker_order, stop_loss_order]
