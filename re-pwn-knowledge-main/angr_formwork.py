import angr   #angr库
import sys    #获取输入输出
import claripy #假设值等等

def main(argv):
    bin_path = argv[1]  #文件名称
    p = angr.Project(bin_path, auto_load_libs=False) # 初始化一个Project对象
    # main函数如果有传参
    '''argc1 = claripy.BVS('argc1',8*8)
    arg = [agrv[1],argc1]'''
    
    # 初始化起始状态
    #init_state = p.factory.entry_state(args=arg) #初始化状态，从入口开始
    start_addr = 0x401606
    init_state = p.factory.blank_state(addr=start_addr) #初始化状态，从addr的地址开始

    #初始化堆（malloc函数创建的容器）
    #malloc函数创建的空间一般地址随机，但是在我们模拟程序时是不可能随机的，所以要事先分配好空间
    '''buffer0 = init_state.regs.rsp -0x100
    buffer0 = init_state.regs.rsp -0x200
    buffer0_addr = 0xabcc8a4
    buffer1_addr = 0xabcc8ac
    init_state.memory.store(buffer0_addr,buffer0,8,endness = p.arch.memory_endness)
    init_state.memory.store(buffer1_addr,buffer1,8,endness = p.arch.memory_endness)'''

    #初始化文件输入
    finename = '1.txt'
    file_size = 0x40
    password1 = init_state.solver.BVS('password1',file_size*8)       #构建密码的符号化向量
    #sim_file = angr.storage.SimFile(finename,content=password1,file_size)  #创建文件向量
    init_state.fs.insert(filename,sim_file)    #插入，能够让打开文件的操作索引到
    
    #初始化栈
    padding_size = 48
    init_state.stack_push(init_state.regs.rbp)
    init_state.regs.rbp = init_state.regs.rsp
    init_state.regs.rsp -= padding_size
    pass1= init_state.solver.BVS('pass1',8*8)
    pass1_addr = init_state.regs.rbp-16
    init_state.memory.store(pass1_addr,pass1,8) #endness指定小段还是大端
    #init_state.stack_push(pass1)  #符号变量压入栈
    

    #初始化寄存器
    #pass1 = claripy.BVS('pass1',64)  #声明变量，64位
    #pass2 = claripy.BVS('pass2',32)  #声明变量，32位
    #pass3 = claripy.BVS('pass3',32)
    #init_state.regs.rax = pass1    #给寄存器赋值


    #初始化内存
    '''p1 = init_state.solver.BVS('p1',8*8)
    p1_addr = 0xa1ba1c0
    init_state.memory.store(p1_addr,p1,8) '''  #往内存中写变量

        
    #创建模拟器开始模拟    
    sm = p.factory.simulation_manager(init_state) #创建模拟器

    #开始搜索
    #为了防止路径爆炸，可以增加约束,然后开始
    '''check_addr = 0x8048565       
    buffer_addr = 0x804a050
    password1 = init_state.solver.BVS('password1',16*8)
    init_state.memory.store(buffer_addr,password1)
    sm = p.factory.simulation_manager(init_state)
    sm.explore(find=check_addr)  
    if sm.found:
        check_state = sm.found[0]
        
        desired_string = 'abcd'
        check_param1 = buffer_addr
        check_param2 = 0x10    #size

        check_bvs = check_state.memory.load(check_param1,check_param2)  #从内存中加载
        check_constraint = desired_string == check_bvs   #增加约束
        check_state.add_constraints(check_constraint)     #加入约束'''
    

    def is_good(state):    #判断是否是找到路径的函数
        return b'success' in state.posix.dumps(1)

    def is_bad(state):     #判断是否是避免的路径函数
        return b'fail' in state.posix.dumps(1)
    sm.explore(find=is_good,avoid=is_bad)   #正常开始

    if sm.found:
        found_state = sm.found[0]   #找到目标
        password1 = found_state.solver.eval(pass1,cast_to = bytes)  #求解pass1的值 cast_to表示求解的类型
        print("solution: {}".format(found_state.posix.dumps(0)))
        print("solution: {}".format(password1))
    else :
        print('No solution')
        
if __name__ == '__main__':
    main(sys.argv)
