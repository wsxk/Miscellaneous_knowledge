import base64

enc ='U1ATIOpkOyWSvGm/YOYFR4!!' #输入的加密字符串

std_base= "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/" #原码
mg_base='yzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/abcdefghijklmnopqrstuvwx'  #换码表

en_trantab=str.maketrans(std_base,mg_base) #std_base到mg_base的映射
de_trantab=str.maketrans(mg_base,std_base) #mg_base 到std_base的映射

flag=base64.b64decode(enc.translate(de_trantab))
print(flag)
