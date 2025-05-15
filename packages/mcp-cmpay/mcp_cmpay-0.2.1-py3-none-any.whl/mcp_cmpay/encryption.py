import binascii

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_der_private_key, load_der_public_key


class RsaUtil:
    @staticmethod
    def rsa_sign(indata, private_key_hex):
        """
        使用RSA私钥对数据进行签名

        参数:
            indata (bytes): 需要签名的数据
            private_key_hex (str): 16进制格式的私钥

        返回:
            str: 16进制格式的签名

        异常:
            Exception: 签名失败时抛出
        """
        try:
            # 将16进制字符串转换为字节
            private_key_bytes = binascii.unhexlify(private_key_hex)

            # 加载私钥(如果没有加密，密码参数传None)
            private_key = load_der_private_key(private_key_bytes, password=None)

            # 创建签名
            signature = private_key.sign(
                indata.encode("utf-8"),
                padding.PKCS1v15(),
                hashes.SHA1()
            )

            # 将签名转换为16进制
            return binascii.hexlify(signature).decode('utf-8')
        except Exception as e:
            raise Exception(f"签名失败: {str(e)}")

    @staticmethod
    def rsa_verify(indata, signature_hex, public_key_bytes):
        """
        验证RSA签名

        参数:
            indata (bytes): 原始数据
            signature_hex (str): 16进制格式的签名
            public_key_bytes (bytes): 字节格式的公钥

        返回:
            bool: 如果签名有效返回True，否则返回False
        """
        try:
            # 将16进制签名转换为字节
            signature = binascii.unhexlify(signature_hex)

            # 加载公钥
            public_key = load_der_public_key(public_key_bytes)

            # 验证签名
            public_key.verify(
                signature,
                indata,
                padding.PKCS1v15(),
                hashes.SHA1()
            )
            return True
        except InvalidSignature:
            return False
        except Exception as e:
            raise Exception(f"验证失败: {str(e)}")

    @staticmethod
    def check_private_key(private_key_hex):
        try:
            # 将16进制字符串转换为字节
            private_key_bytes = binascii.unhexlify(private_key_hex)

            # 尝试加载私钥
            private_key = load_der_private_key(private_key_bytes, password=None)

            # 获取私钥的一些信息
            key_size = private_key.key_size
            public_numbers = private_key.public_key().public_numbers()

            return {
                "有效": True,
                "密钥大小": key_size,
                "公钥指数": public_numbers.e
            }
        except Exception as e:
            return {
                "有效": False,
                "错误": str(e)
            }
