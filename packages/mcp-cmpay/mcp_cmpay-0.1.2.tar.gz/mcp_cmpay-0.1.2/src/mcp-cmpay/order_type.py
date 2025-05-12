from enum import Enum

class OrderType(Enum):
    WAP_DIRECT_PAY = "WAPDirectPayConfirm"
    ORDER_QUERY = "OrderQuery"
    ORDER_REFUND = "OrderRefund"
    MERCHANT_REFUND_QUERY = "merchantOrderRefundQuery"
