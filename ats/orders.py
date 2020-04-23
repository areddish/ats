from ibapi.order import Order
from enum import Enum
from ats.sms.twilio import send_notification

#testing


# Need an order log ot monitor all information
# need a db to hold all orders
# order state machine
# capture the executions too

class OrderType(Enum):
    BUY = 1
    SELL = 2

class OrderStatus(Enum):
    pending_cancel = "PendingCancel"
    cancel = "Cancelled"
    presubmit = "Presubmitted"

next_order_id = 1

class Order(Order):
    def __init__(self, contract, owner):
        super().__init__()
        self.contract = contract
        self.manager = owner
        self.status = None
        self.on_filled = None
        self.on_cancel = None
        self.notified = False

    def place(self):
        self.manager.place_order(self)

    def update_price(self, price):
        # TODO: this should be handled via a if or inheritance
        self.lmtPrice = price
        self.manager.place_order(self)

    def cancel(self):
        self.manager.cancel_order(self)

    def notify_cancelled(self):
        if self.on_cancel:
            self.on_cancel()

    def notify_filled(self, qty, avgFillPrice):
        if not self.notified:
            send_notification(f"{self.action}: {self.contract.symbol} {qty} @ ${avgFillPrice}")
            if self.on_filled:
                self.on_filled(avgFillPrice)
            self.notified = True

    def update(self, status, filled, remaining, avgFilPrice):
        if status != self.status:
            self.status = status
            if status == "Filled":
                self.notify_filled(filled, avgFilPrice)

class OrderManager(object):
    def __init__(self, trader):
        self.orders = {}
        self.next_valid_order_id = None
        self.trader = trader
        self.executions = {}
        self.commissions = {}

    def associate_account(self, account):
        self.account = account

    def get_open_orders():
        # Synchronize our orders against open
        pass

    def get_commissions_paid():
        return sum(map(lambda x: x.Commission, self.commissions))

    def on_error(self, reqId: int, errorCode: int, errorString: str):
        if reqId not in self.orders:
            return False

        print (f"ORDER ERROR: {reqId} {self.orders[reqId].contract.symbol} {errorCode} {errorString}")
        return True

    def on_order_status(self, orderId: int, status: str, filled: float,
                    remaining: float, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        # TODO:
        print("ORDER: STATUS:", locals())
        order = self.orders[orderId]
        order.update(status, filled, remaining, avgFillPrice)

    def on_open_order(self, *args):
        pass

    def on_open_order_end(self):
        pass

    def on_exec_details(self, reqId, contract, execution):
        print ("ORDER: EXEC: ", reqId, contract, execution)
        self.executions[execution.execId] = execution
        return reqId in self.orders

    def on_commision_report(self, commissionReport):
        print ("ORDER: COMMISSION: ", commissionReport)
        self.commissions[commissionReport.execId] = commissionReport
        
        return commissionReport.execId in self.executions

    def place_order(self, order):
        self.orders[order.orderId] = order
        self.trader.place_order(order)

    def cancel_order(self, order):
        self.trader.cancel_order(order)

    def create_order(self, contract, qty, order_type):
        order = Order(contract, self)
        order.orderId = self._inc_order_id()
        order.totalQuantity = qty
        order.action = "BUY" if order_type == OrderType.BUY else "SELL"
        order.outsideRth = True
        order.transmit = True
        return order


    def create_market_order(self, contract, qty, order_type):
        order = self.create_order(contract, qty, order_type)
        order.orderType = "MKT"
        return order


    def create_limit_order(self, contract, qty, order_type, price):
        order = self.create_order(contract, qty, order_type)
        order.orderType = "LMT"
        order.lmtPrice = price
        return order


    def create_stop_order(self, contract, qty, order_type, price):
        order = self.create_order(contract, qty, order_type)
        order.orderType = "STP"
        order.auxPrice = price
        return order


    def create_bracket_order(self, contract, qty, profit_price, stop_loss_price):
        market_order = self.create_market_order(contract, qty, OrderType.BUY)
        profit_taker_order = self.create_limit_order(contract, qty, OrderType.SELL, profit_price)
        stop_loss_order = self.create_stop_order(contract, qty, OrderType.SELL, stop_loss_price)

        market_order.transmit = False
        profit_taker_order.transmit = False

        profit_taker_order.parentId = market_order.orderId
        stop_loss_order.parentId = market_order.orderId

        return [market_order, profit_taker_order, stop_loss_order]

    def _inc_order_id(self):
        result = self.next_valid_order_id
        self.next_valid_order_id += 1
        return result
