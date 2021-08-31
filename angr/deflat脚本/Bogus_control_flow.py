from idc_bc695 import *
st = 0x0000000000401117
end = 0x0000000000402144

def patch_nop(start,end):
    for i in range(start,end):
        PatchByte(i, 0x90)		#修改指定地址处的指令  0x90是最简单的1字节nop
 
def next_instr(addr):
    return addr+ItemSize(addr)		#ItemSize获取指令或数据长度，这个函数的作用就是去往下一条指令
    

 
addr = st
while(addr<end):
    next = next_instr(addr)
    if "ds:dword_603054" in GetDisasm(addr):	#GetDisasm(addr)得到addr的反汇编语句
        while(True):
            addr = next
            next = next_instr(addr)
            if "jnz" in GetDisasm(addr):
                dest = GetOperandValue(addr, 0)		#得到操作数，就是指令后的数
                PatchByte(addr, 0xe9)
                PatchByte(addr+5, 0x90) 
                offset = dest - (addr + 5)
                PatchDword(addr + 1, offset)
                print("patch bcf: 0x%x"%addr)
                addr = next
                break
    else:
        addr = next
