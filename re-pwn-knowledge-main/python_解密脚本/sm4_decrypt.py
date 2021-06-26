from Crypto.Util.number import bytes_to_long,long_to_bytes


    
# S盒
SboxTable = \
[
    0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
    0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
    0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
    0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
    0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
    0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
    0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
    0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
    0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
    0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
    0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
    0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
    0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
    0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
    0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
    0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48,
]
# 常数FK
FK = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc] ; ENCRYPT = 0 ;DECRYPT = 1
# 固定参数CK
CK = \
[
    0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,
    0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
    0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
    0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
    0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
    0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
    0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
    0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279
]
def padding(data):   #填充
    print ("plaintext:\t", bytes (data))
    file_data_list = list(data)
    lenth = len (file_data_list)
    #print ("data lenth:", lenth)
    remainder = lenth % 16
    if remainder != 0:
        i=16-remainder               #i为需要填充的位数
        #print ("padding numbers = ", i)
        for j in range(i):
           file_data_list.append(i)  #填充 char 0-(i-1)
    if remainder == 0:
        for k in range(16):
            file_data_list.append (0x08)  #刚好的话 填充0x08
    print("after PKCS5 padding:",file_data_list)
    return file_data_list
def list_4_8_to_int32(key_data):  # 列表4个8位，组成32位
    return int ((key_data[0] << 24) | (key_data[1] << 16) | (key_data[2] << 8) | (key_data[3]))
def n32_to_list4_8(n):  #把n分别取32位的每8位放入列表
    return [int ((n >> 24) & 0xff), int ((n >> 16) & 0xff), int ((n >> 8) & 0xff), int ((n) & 0xff)]
#循环左移
def shift_left_n(x, n):
    return int (int (x << n) & 0xffffffff)
def shift_logical_left(x, n):
    return shift_left_n (x, n) | int ((x >> (32 - n)) & 0xffffffff)  #两步合在一起实现了循环左移n位
def XOR(a, b):
    return list (map (lambda x, y: x ^ y, a, b))
#s盒查找
def sbox(idx):
    return SboxTable[idx]
def extended_key_LB(ka):      #拓展密钥算法LB
    a = n32_to_list4_8 (ka)                #a是ka的每8位组成的列表
    b = [sbox (i) for i in a]               #在s盒中每8位查找后，放入列表b，再组合成int bb
    bb = list_4_8_to_int32 (b)
    rk = bb ^ (shift_logical_left (bb, 13)) ^ (shift_logical_left (bb, 23))
    return rk
def linear_transform_L(ka):      #线性变换L
    a = n32_to_list4_8 (ka)
    b = [sbox (i) for i in a]
    bb = list_4_8_to_int32 (b)     #bb是经过s盒变换的32位数
    return bb ^ (shift_logical_left (bb, 2)) ^ (shift_logical_left (bb, 10)) ^ (shift_logical_left (bb, 18)) ^ (shift_logical_left (bb, 24)) #书上公式
def sm4_round_function(x0, x1, x2, x3, rk):   #轮函数
    return (x0 ^ linear_transform_L (x1 ^ x2 ^ x3 ^ rk))
class Sm4 (object):
    def __init__(self):
        self.sk = [0] * 32
        self.mode = ENCRYPT
    def sm4_set_key(self, key_data, mode):    #先算出拓展密钥
        self.extended_key_last (key_data, mode)
    def extended_key_last(self, key, mode):   #密钥扩展算法
        MK = [0, 0, 0, 0]
        k = [0] * 36
        MK[0] = list_4_8_to_int32 (key[0:4])
        MK[1] = list_4_8_to_int32 (key[4:8])
        MK[2] = list_4_8_to_int32 (key[8:12])
        MK[3] = list_4_8_to_int32 (key[12:16])
        k[0:4] = XOR (MK, FK)
        for i in range (32):
            k[i + 4] = k[i] ^ (extended_key_LB (k[i + 1] ^ k[i + 2] ^ k[i + 3] ^ CK[i]))
        self.sk = k[4:]   #生成的32轮子密钥放到sk中
        self.mode = mode
        if mode == DECRYPT:      #解密时rki逆序
            self.sk.reverse ()
    def sm4_one_round(self, sk, in_put):   #一轮算法 ，4个32位的字=128bit=16个字节（8*16）
        item = [list_4_8_to_int32 (in_put[0:4]), list_4_8_to_int32 (in_put[4:8]), list_4_8_to_int32 (in_put[8:12]),
                list_4_8_to_int32 (in_put[12:16])]    #4字节一个字，把每4个字节变成32位的int
        x=item
        for i in range (32):
            temp=x[3]
            x[3] = sm4_round_function (x[0], x[1], x[2], x[3], sk[i]) #x[3]成为x[4]
            x[0]=x[1]
            x[1]=x[2]
            x[2]=temp
            print("%dround----->"%(i+1),"key:%-12d\n"%sk[i],"result：",x)
        res=x
        # res = reduce (lambda x, y: [x[1], x[2], x[3], sm4_round_function (x[0], x[1], x[2], x[3], y)],sk, item) #32轮循环加密
        res.reverse ()
        rev = map (n32_to_list4_8, res)
        out_put = []
        [out_put.extend (_) for _ in rev]
        return out_put
    def encrypt(self, input_data):
        # 块加密
        output_data = []
        tmp = [input_data[i:i + 16] for i in range (0, len (input_data), 16)]  #输入数据分块
        [output_data.extend (each) for each in map (lambda x: self.sm4_one_round (self.sk, x), tmp)]
        return output_data
def encrypt(mode, key, data):
    sm4_d = Sm4 ()
    sm4_d.sm4_set_key (key, mode)
    en_data = sm4_d.encrypt (data)
    return en_data
def sm4_crypt_cbc(mode, key, iv, data):
    sm4_d = Sm4 ()
    sm4_d.sm4_set_key (key, mode)
    en_data = sm4_d.sm4_crypt_cbc (iv, data)
    return en_data
if __name__ == "__main__":
    key_data=[ord(c) for c in "Ez_5M4_C1pH@r!!!"]
    
    en_data=b"\xEA\x63\x58\xB7\x8C\xE2\xA1\xE9\xC5\x29\x8F\x53\xE8\x08\x32\x59\xAF\x1B\x67\xAE\xD9\xDA\xCF\xC4\x72\xFF\xB1\xEC\x76\x73\xF3\x06"
    sm4_d = Sm4 ()
    sm4_d.sm4_set_key (key_data, DECRYPT)
    de_data = sm4_d.encrypt (en_data)
    flag=''.join(list(map(chr,de_data)))
    print(flag)
    print(len(en_data))
