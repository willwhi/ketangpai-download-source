from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad 
import base64 
 
class AESCipher:
    def __init__(self, key: str, iv: str, padding_style : str='pkcs7'):
        """
        初始化加密器 
        :param key: 16字符的UTF-8字符串（128位）
        :param iv: 16字符的UTF-8字符串（128位）
        """
        self.block_size  = AES.block_size  
        self.key  = self.__process_key(key)
        self.iv  = self.__process_iv(iv)
        self.style = padding_style
    
    def __process_key(self, key_str: str) -> bytes:
        """密钥标准化处理"""
        key_bytes = key_str.encode('utf-8') 
        if len(key_bytes) != 16:
            raise ValueError("密钥必须为16字节长度")
        return key_bytes 
    
    def __process_iv(self, iv_str: str) -> bytes:
        """IV标准化处理"""
        iv_bytes = iv_str.encode('utf-8') 
        if len(iv_bytes) != 16:
            raise ValueError("IV必须为16字节长度")
        return iv_bytes 
    
    def encrypt(self, plaintext: str) -> str:
        """PKCS7填充的CBC模式加密"""
        # 数据预处理 
        plain_bytes = plaintext.encode('utf-8') 
        padded_data = pad(plain_bytes, self.block_size,  self.style)
        
        # 创建加密器 
        cipher = AES.new(self.key,  AES.MODE_CBC, iv=self.iv) 
        
        # 执行加密 
        cipher_bytes = cipher.encrypt(padded_data) 
        
        # Base64编码 
        return base64.b64encode(cipher_bytes).decode('utf-8')

def encrypt(key, iv, padding_style,plaintext):
    encryptor = AESCipher(key, iv, padding_style)
    return encryptor.encrypt(plaintext)
    