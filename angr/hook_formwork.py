import angr
import sys
import claripy

def main(argv):
    bin_path = argv[1]
    p = angr.Project(bin_path)
    #p.hook_symbol(0x100000F0A, angr.SIM_PROCEDURES["libc"]["strlen"]())
    #p.hook_symbol(0x100000EF8, angr.SIM_PROCEDURES["libc"]["memset"]())
    #p.hook_symbol(0x100000EFE, angr.SIM_PROCEDURES["libc"]["printf"]())
    #p.hook_symbol(0x100000F04, angr.SIM_PROCEDURES["posix"]["read"]())
    #p.hook_symbol(0x100000F10, angr.SIM_PROCEDURES["libc"]["strncmp"]())
    init_state = p.factory.entry_state()

    check_addr = 0x8048683   #要hook的地址
    check_skip_size = 5           #与要hook的指令的字节大小相同

    @p.hook(check_addr,length=check_skip_size)
    def check_hook(state):                       #等效于check_hook = p.hook(check_daar,length=check_skip_size,check_hook)
        user_input_addr = 0x8041054
        user_input_length = 0x10
        
        user_input_bvs = state.memory.load(user_input_addr,user_input_length)

        desired = 'wxk'
        state.regs.eax = claripy.if(desired==user_input_bvs,claripy.BVV(1,32),claripy.BVV(0,32)) #32表示32位

    def is_good(state):
        return b'success' in state.posix.dumps(1)

    def is_bad(state):
        return b'fail' in state.posix.dumps(1)

    sm = p.factory.simgr(init_state)
    sm.explore(find=is_good,avoid=is_bad)

    if sm.found:
        found_state = sm.found[0]
        print('solution:{}'.format(found_state.posix.dumps(0)))

if __name__ == '__main__':
    main(sys.argv)
