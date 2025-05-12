import os

TEST_URL = "https://uatipos.10086.cn/ips/cmpayService"
PROD_URL = "https://ipos.10086.cn/ips/cmpayService"
NOTIFY_URL = "http://10.176.9.219:8527/v1/consume/notify/unified-notify"
# 签名类型：RSA或MD5
SIGN_TYPE = "RSA"
VERSION = "2.0.0"
QUERY_REFUND_VERSION = "2.0.8"

# 交易有效期
PERIOD = 60
# 交易有效期单位（分钟）
PERIOD_UNIT = "00"
# 币种（00：人民币）
CURRENCY = "00"


def get_config(key: str, default: str) -> str:
    value = os.environ.get(key)
    if value is None:
        print(f"警告: 环境变量 {key} 未设置，使用默认值")
    return value or default


MERCHANT_ID = get_config('MERCHANT_ID', "")
SIGN_KEY = get_config('SIGN_KEY', "")
