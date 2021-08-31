from Crypto.Cipher import AES

#AES ECB模式解密
key =[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]    #密钥
ciphertext = [97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97] #密文
aes = AES.new(key=bytes(key),mode=AES.MODE_ECB)  #mode是设置模式
string = bytes(ciphertext)
print(aes.decrypt(string))

#AES CBC模式解密
iv = []
key = []
cipher=[]
aes = AES.new(key,AES.MODE_CBC,iv)
flag= aes.decrypt(cipher)
print(flag)
