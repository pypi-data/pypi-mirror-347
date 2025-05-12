from mcp.server.fastmcp import FastMCP

from api_calls import create_wap_payment_order, query_wep_payment_order, refund_payment_order, \
    query_refund_payment_order

mcp = FastMCP('CMPayServer')


# mcp = FastMCP(name='CMPayServer',
#               port=8000,
#               host='0.0.0.0',
#               description='CMPay Server',
#               sse_path='/sse')


@mcp.tool()
async def create_wap_cmpay_order(
        product_name: str,
        order_id: str,
        amount: int,
        order_date: str
) -> str:
    """
    创建一笔和包订单，返回带有支付链接的 Markdown 文本，该链接在电脑浏览器中打开后会展示支付页面，用户可点击打开网页进行登录支付。

    Args:
        product_name (str): 商品名称（必填）,只能是数字、大小写字母。
        order_id (str): 商户订单号，需与amount对应且唯一（必填），商户系统内部订单号，要求10-32个字符内，只能是数字、大小写字母，且在同一个商户编号下唯一。
        amount (int): 订单金额，单位为分，如"1000"代表10元（必填）。
        order_date (str): 商户订单日期，格式为YYYYMMDD（必填），通常为当天日期。

    Returns:
        dict: 包含支付链接、状态码、消息的响应结果等。
    """

    response = await create_wap_payment_order(product_name, order_id, amount, order_date)

    return f"""
    商户编号：{response.get("merchantId")}
    商户请求号：{response.get("requestId")}
    签名方式：{response.get("signType")}
    接口类型：{response.get("type")}
    版本号：{response.get("version")}
    返回码：{response.get("returnCode")}
    支付地址：{response.get("payUrl")}
    签名值：{response.get("hmac")}
    返回码描述信息：{response.get("message")}
    """


@mcp.tool()
async def query_wep_cmpay_order(order_id: str) -> str:
    """
    查询一笔和包订单，并返回带有订单信息的文本。

    Args:
        order_id (str): 商户订单号（必填），商户系统内部订单号，要求10-32个字符内，只能是数字、大小写字母，且在同一个商户编号下唯一。

    Returns:
        dict: 返回带有订单信息的文本。
    """

    response = await query_wep_payment_order(order_id)

    return f"""
    商户编号：{response.get("merchantId")}
    流水号：{response.get("payNo")}
    返回码：{response.get("returnCode")}
    返回码描述信息：{response.get("message")}
    签名方式：{response.get("signType")}
    接口类型：{response.get("type")}
    版本号：{response.get("version")}
    支付金额：{response.get("amount")}
    商户订单号：{response.get("orderId")}
    支付时间：{response.get("payDate")}
    支付结果：{response.get("status")}
    """


@mcp.tool()
async def refund_cmpay_order(order_id: str, amount: int, payNo: str) -> str:
    """
    对交易发起退款，并返回退款状态和退款金额。

    Args:
        order_id (str): 商户订单号（必填），为原支付时的商户订单号。
        amount (int): 退款金额（必填），单位为分，必须小于等于原支付金额。
        payNo (str): 流水号（必填），从订单查询接口（query_wep_payment_order）获取该字段值。

    Returns:
        dict: 返回带有退款信息的文本。
    """

    response = await refund_payment_order(order_id, amount, payNo)

    return f"""
    商户编号：{response.get("merchantId")}
    流水号：{response.get("payNo")}
    返回码：{response.get("returnCode")}
    返回码描述信息：{response.get("message")}
    签名方式：{response.get("signType")}
    接口类型：{response.get("type")}
    版本号：{response.get("version")}
    退款金额：{response.get("amount")}
    商户订单号：{response.get("orderId")}
    退款结果：{response.get("status")}
    """


@mcp.tool()
async def query_refund_cmpay_order(order_id: str, order_date: str) -> str:
    """
    查询一笔和包退款，并返回退款状态和退款金额。

    Args:
        order_id (str): 商户订单号（必填），为原支付时的商户订单号。
        order_date (str): 商户订单日期，格式为YYYYMMDD（必填），从订单查询接口（query_wep_payment_order）获取该字段。

    Returns:
        dict: 返回带有退款信息的文本。
            订单状态(orderStatus)有如下几种枚举值：
                BA ：直接支付预登记
                BB：直接支付用户信息补录成功
                BC：直接支付发送金额补录申请成功
                BD：直接支付订单支付成功
                RP：部分退款
                RF：全部退款
            退款状态(refundStatus)有如下几种枚举值：
                P：处理中
                S：成功
                F：处理失败
    """

    response = await query_refund_payment_order(order_id, order_date)

    return f"""
    商户编号：{response.get("merchantId")}
    商户请求号：{response.get("merchantRequestNo")}
    签名方式：{response.get("signType")}
    接口类型：{response.get("type")}
    版本号：{response.get("version")}
    返回码：{response.get("returnCode")}
    返回码描述信息：{response.get("message")}
    签名值：{response.get("hmac")}
    商户订单号：{response.get("merchantOrderNo")}
    订单状态：{response.get("orderStatus")}
    退款状态：{response.get("refundStatus")}
    """


# if __name__ == "__main__":
#     # Initialize and run the server
#     try:
#         mcp.run(transport='sse')
#     except Exception as e:
#         print(f"Error: {e}")
#
#     mcp.run(transport='stdio')

def main():
    mcp.run()


if __name__ == '__main__':
    main()
