import base64

enc ='yQXHyBvN3g/81gv51QXG1QTBxRr/yvXK1hC=' #输入的加密字符串

std_base= "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/" #原码
mg_base='@,.1fgvw#`/2ehux$~\"3dity%_;4cjsz^+{5bkrA&=}6alqB*-[70mpC()]89noD'  #换码表

en_trantab=str.maketrans(std_base,mg_base) #std_base到mg_base的映射
de_trantab=str.maketrans(mg_base,std_base) #mg_base 到std_base的映射

flag=base64.b64decode(enc.translate(de_trantab))
print(flag)
