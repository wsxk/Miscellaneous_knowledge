from hashlib import md5
from binascii import *

text = b'135312467n'        # binascii
text_md5 = md5(text)        #md5
text_md5_hex = text_md5.hexdigest()#str类型 十六进制
print(text_md5_hex)

text_md5_hex_bina = unhexlify(text_md5_hex)  #str(bina) hex to 二进制字符串
print(text_md5_hex_bina)
print(hexlify(text_md5_hex_bina))   #二进制字符串 转 bina hex

