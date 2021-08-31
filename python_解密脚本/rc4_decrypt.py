key = 'th1s_1s_k3y!!!!!'#密钥
key_list=[]
for i in range(len(key)):
    key_list.append(ord(key[i]))
#print(key_list)

v0 = [0 for i in range(0x100)]
v1 = [0 for i in range(0x100)]
for i in range(0x100):
    v0[i] = 0x100-i
    v1[i] = key_list[i%len(key)]
v2 = 0
v7_1=0
while v2<0x100:
    v7_1 = (v0[v2]+v7_1+v1[v2])%0x100
    v8 = v0[v2]
    v0[v2] = v0[v7_1]
    v0[v7_1]=v8
    v2+=1
#print(v0)

#密文
target = [0x8B, 210, 0xD9, 93, 0x95, 0xFF, 0x7E, 0x5F, 41, 86, 18, 0xB9, 0xEF, 0xEC, 0x8B, 0xD0, 69]

i = 0
a=0
b=0
c=0
while i < len(target):
    a = (a+1)%0x100
    b = (v0[a]+b)%0x100
    c = v0[b]
    v0[b] = v0[a]
    v0[a] = c
    target[i]= target[i]^v0[(v0[a]+v0[b])%0x100]
    i+=1
for i in range(len(target)):
    print(chr(target[i]),end='')
