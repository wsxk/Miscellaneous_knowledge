def encrypt(rounds, v, k):
    v0 = v[0]
    v1 = v[1]
    x = 0
    delta = 0x9E3779B9
    for i in range(rounds):
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (x + k[x & 3])
        v0 = v0 & 0xFFFFFFFF
        x += delta
        x = x & 0xFFFFFFFF
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (x + k[(x >> 11) & 3])
        v1 = v1 & 0xFFFFFFFF
    v[0] = v0
    v[1] = v1
    return v
def decrypt(rounds, v, k):
    v0 = v[0]
    v1 = v[1]
    delta = 0x9E3779B9
    x = delta * rounds
    for i in range(rounds):
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (x + k[(x >> 11) & 3])
        v1 = v1 & 0xFFFFFFFF
        x -= delta
        x = x & 0xFFFFFFFF
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (x + k[x & 3])
        v0 = v0 & 0xFFFFFFFF
    v[0] = v0
    v[1] = v1
    return v
if __name__ == '__main__':
    plain = [1, 2]      #加密的2个无符号32位整数
    key = [2, 2, 3, 4]   #加密解密密钥，4个32位无符号整数，即128位
    rounds = 32             #加密轮数
    encrypted = encrypt(rounds, plain, key)
    print(encrypted)
    decrypted = decrypt(rounds, encrypted, key)
    print(decrypted)
