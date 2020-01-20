from ibapi.order import Order
from enum import Enum

#testing

class OrderType(Enum):
    BUY = 1
    SELL = 2


next_order_id = 1


class OrderManager(object):
    def __init__(self, trader):
        self.orders = {}
        self.next_valid_order_id = None
        self.trader = trader

    def on_order_status(*args):
        pass

    def on_open_order(*args):
        pass

    def on_open_order_end():
        pass

    def place_order(self, order):
        self.orders[order.irderId] = order
        self.trader.placeOrder(order.orderId, order.contract, order)

    def create_order(qty, order_type):
        order = Order()
        order.orderId = _inc_order_id()
        order.totalQuantity = qty
        order.action = "BUY" if order_type == OrderType.BUY else "SELL"
        order.transmit = True
        return order


    def create_market_order(qty, order_type):
        order = create_order(qty, order_type)
        order.orderType = "MKT"
        return order


    def create_limit_order(qty, order_type, price):
        order = create_order(qty, order_type)
        order.orderType = "LMT"
        order.lmtPrice = price
        return order


    def create_stop_order(qty, order_type, price):
        order = create_order(qty, order_type)
        order.orderType = "STP"
        order.auxPrice = price
        return order


    def create_bracket_order(qty, profit_price, stop_loss_price):
        market_order = create_market_order(qty, OrderType.BUY)
        profit_taker_order = create_limit_order(qty, OrderType.SELL, profit_price)
        stop_loss_order = create_stop_order(qty, OrderType.SELL, stop_loss_price)

        market_order.transmit = False
        profit_taker_order.transmit = False

        profit_taker_order.parentId = market_order.orderId
        stop_loss_order.parentId = market_order.orderId

        return [market_order, profit_taker_order, stop_loss_order]

    def _inc_order_id():
        result = self.next_valid_order_id
        self.next_valid_order_id += 1
        return result
