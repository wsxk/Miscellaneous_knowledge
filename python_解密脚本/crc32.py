from idc_bc695 import *

addr = 0x402170
check = []
flag = []
key = 0xB0004B7679FA26B3
for i in range(6):
    check.append(Qword(addr+8*i))

for i in range(6):
    s = check[i]
    for j in range(64):
        sign = s&1
        if sign==1:
            s ^= key
        s = s>>1
        if sign ==1:
            s |= 0x8000000000000000
    for j in range(8):
        flag.append(s&0xff) 
        s = s>>8
print(bytes(flag))

