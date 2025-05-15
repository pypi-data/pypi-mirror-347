# 中国移动支付服务（MCP）

中国移动支付(China Mobile Pay) MCP Server 服务，智能体开发者可轻松接入中移支付服务，目前提供了订单创建、订单查询、申请退款及退款查询功能。

## 主要功能

  - 订单创建`create_wap_payment_order`
    - 创建网页支付订单。
    - 输入：
      - product_name (str): 商品名称。
      - order_id (str): 商户订单号。
      - amount (int): 订单金额，单位为分。
    - 输出：
      - 订单信息，支付链接等。

  - 订单查询`query_wep_payment_order`
    - 交易支付状态信息。
    - 输入：
      - order_id (str): 商户订单号。
    - 输出：
      - 订单信息，支付时间、支付结果、支付金额等。

  - 申请退款`refund_payment_order`
    - 对交易进行退款操作。
    - 输入：
      - order_id (str): 商户订单号。
      - amount (int): 退款金额。
      - payNo (str): 流水号。
    - 输出：
      - 退款信息，退款时间、退款金额等。

  - 退款查询`query_refund_payment_order`
    - 交易订单退款信息查询。
    - 输入：
      - order_id (str): 商户订单号。
      - order_date (str): 商户订单日期。
    - 输出：
      - 退款信息，退款状态等。

## 环境变量

在和包商户端进行申请，配置以下环境变量：
  - `MERCHANT_ID`: 商户ID。
  - `SIGN_KEY`: 签名密钥。

## 示例用法

`mcp-cmpay`应由 MCP 客户端启动，因此必须进行相应的配置。对于 Claude Desktop，配置可以如下所示：

```json
{
    "mcpServers": {
        "mcp-server-cmpay": {
            "command": "uvx",
            "args": [
                "mcp-cmpay"
            ],
            "env": {
                "MERCHANT_ID": "<YOUR_MERCHANT_ID>",
                "SIGN_KEY": "<YOUR_SIGN_KEY>"
            }
        }
    }
}
```
