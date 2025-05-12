import asyncio
from typing import Any
from urllib.parse import parse_qs, urljoin

import httpx

from config import MERCHANT_ID, SIGN_TYPE, SIGN_KEY, VERSION, PROD_URL, NOTIFY_URL, QUERY_REFUND_VERSION, PERIOD, \
    PERIOD_UNIT, CURRENCY
from encryption import RsaUtil
from order_type import OrderType


async def create_wap_payment_order(product_name: str, order_id: str, amount: int, order_date: str) -> dict[
                                                                                                          str, Any] | None:
    order_type = OrderType.WAP_DIRECT_PAY.value

    sign_data = (NOTIFY_URL + MERCHANT_ID + order_id + SIGN_TYPE + order_type + VERSION + str(amount) + CURRENCY
                 + order_date + order_id + str(PERIOD) + PERIOD_UNIT + product_name)
    hmac = RsaUtil.rsa_sign(sign_data, SIGN_KEY)

    data = {
        "notifyUrl": NOTIFY_URL,
        "merchantId": MERCHANT_ID,
        "requestId": order_id,
        "signType": SIGN_TYPE,
        "type": order_type,
        "version": VERSION,
        "hmac": hmac,
        "amount": str(amount),
        "currency": CURRENCY,
        "orderDate": order_date,
        "orderId": order_id,
        "period": PERIOD,
        "periodUnit": PERIOD_UNIT,
        "productName": product_name
    }

    result = await _make_request(data)
    if result and "payUrl" in result:
        result["payUrl"] = format_pay_url(result["payUrl"])
    return result


async def query_wep_payment_order(order_id: str) -> dict[str, Any] | None:
    order_type = OrderType.ORDER_QUERY.value

    sign_data = MERCHANT_ID + order_id + SIGN_TYPE + order_type + VERSION + order_id
    hmac = RsaUtil.rsa_sign(sign_data, SIGN_KEY)

    data = {
        "merchantId": MERCHANT_ID,
        "requestId": order_id,
        "signType": SIGN_TYPE,
        "type": order_type,
        "version": VERSION,
        "orderId": order_id,
        "hmac": hmac
    }

    return await _make_request(data)


async def refund_payment_order(order_id: str, amount: int, payNo: str) -> dict[str, Any] | None:
    order_type = OrderType.ORDER_REFUND.value
    sign_data = MERCHANT_ID + payNo + SIGN_TYPE + order_type + VERSION + order_id + str(amount)
    hmac = RsaUtil.rsa_sign(sign_data, SIGN_KEY)

    data = {
        "merchantId": MERCHANT_ID,
        "requestId": payNo,
        "signType": SIGN_TYPE,
        "type": order_type,
        "version": VERSION,
        "orderId": order_id,
        "amount": str(amount),
        "hmac": hmac
    }

    return await _make_request(data)


async def query_refund_payment_order(order_id: str, order_date: str) -> dict[str, Any] | None:
    order_type = OrderType.MERCHANT_REFUND_QUERY.value
    version = QUERY_REFUND_VERSION
    sign_data = (MERCHANT_ID + order_id + SIGN_TYPE + order_type + version + order_id + order_date)
    hmac = RsaUtil.rsa_sign(sign_data, SIGN_KEY)

    data = {
        "merchantId": MERCHANT_ID,
        "merchantRequestNo": order_id,
        "signType": SIGN_TYPE,
        "type": order_type,
        "version": version,
        "hmac": hmac,
        "merchantOrderNo": order_id,
        "merchantOrderDate": order_date
    }

    return await _make_request(data)


async def _make_request(data: dict) -> dict[str, Any] | None:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url=PROD_URL, data=data, headers=headers)
            response.raise_for_status()
            parsed_dict = parse_qs(response.text)
            return {key: value[0] for key, value in parsed_dict.items()}
        except Exception as e:
            print(f"Error: {e}")
            return None


def format_pay_url(pay_url: str) -> str:
    parts = pay_url.split("<hi:$$>")
    url_part = parts[0].split("<hi:=>")[1]
    session_id = parts[2].split("<hi:=>")[1]
    return urljoin(url_part, "?sessionId=" + session_id)


if __name__ == '__main__':
    async def main():
        response = await create_wap_payment_order(product_name="PoemService", order_id="Poem20250506ABC123", amount=100,
                                                  order_date="20240506")
        # response = await query_wep_payment_order(order_id="SPRINGPOEM20250506172140")
        # response = await refund_payment_order(order_id="SPRING20250506ABC", amount=2, payNo="880000043281949712")
        # response = await query_refund_payment_order(order_id="SPRINGPOEM20250506172140", order_date="20250506")
        print(response)


    asyncio.run(main())
