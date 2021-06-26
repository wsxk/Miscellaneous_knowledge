 def handle_exception(self, successors, engine, exception):
        # don't bother handling non-vex exceptions 不要费心处理非非自愿性例外
        if engine is not self.project.factory.default_engine:
            raise exception
        # don't bother handling symbolic-address exceptions 不要烦恼处理符号地址异常
        if type(exception) is SimSegfaultException:
            if exception.original_addr is not None and exception.original_addr.symbolic:
                raise exception

        _l.debug("Handling exception from block at %#x: %r", successors.addr, exception)

        # If our state was just living out the rest of an unsatisfiable guard, discard it 如果我们的状态只是在维持一个无法令人满意的警卫人员的其余部分，那就把它丢掉
        # it's possible this is incomplete because of implicit constraints added by memory or ccalls...由于内存或调用增加了隐式约束，因此这可能是不完整的
        if not successors.initial_state.satisfiable(extra_constraints=(exception.guard,)):
            _l.debug("... NOT handling unreachable exception")
            successors.processed = True
            return

        # we'll need to wind up to the exception to get the correct state to resume from...我们需要处理异常以获取正确的状态以从中恢复
        # exc will be a SimError, for sure 肯定是模拟器错误
        # executed_instruction_count is incremented when we see an imark BUT it starts at -1, so this is the correct val当我们看到imark但它从-1开始时，Executed_instruction_count就增加了，所以这是正确的值
        num_inst = exception.executed_instruction_count
        if num_inst >= 1:
            # scary...害怕
            try:
                r = self.project.factory.default_engine.process(successors.initial_state, num_inst=num_inst)
                if len(r.flat_successors) != 1:
                    if exception.guard.is_true():
                        _l.error("Got %d successors while re-executing %d instructions at %#x "
                                 "for unconditional exception windup",
                                 len(r.flat_successors), num_inst, successors.initial_state.addr)
                        raise exception
                    # Try to figure out which successor is ours...尝试找出我们的继任者
                    _, _, canon_guard = exception.guard.canonicalize()
                    for possible_succ in r.flat_successors:
                        _, _, possible_guard = possible_succ.recent_events[-1].constraint.canonicalize()
                        if canon_guard is possible_guard:
                            exc_state = possible_succ
                            break
                    else:
                        _l.error("None of the %d successors while re-executing %d instructions at %#x "
                                 "for conditional exception windup matched guard",
                                 len(r.flat_successors), num_inst, successors.initial_state.addr)
                        raise exception

                else:
                    exc_state = r.flat_successors[0]
            except:
                # lol no哈哈，不
                _l.error("Got some weirdo error while re-executing %d instructions at %#x "
                         "for exception windup", num_inst, successors.initial_state.addr)
                raise exception
        else:
            # duplicate the history-cycle code here...在此处复制历史记录周期代码
            exc_state = successors.initial_state.copy()
            exc_state.register_plugin('history', successors.initial_state.history.make_child())
            exc_state.history.recent_bbl_addrs.append(successors.initial_state.addr)

        _l.debug("... wound up state to %#x", exc_state.addr)

        # first check that we actually have an exception handler首先检查我们是否确实有一个异常处理程序
        # we check is_true since if it's symbolic this is exploitable maybe?我们检查is_true，因为如果它是象征性的，这可能是可利用的
        tib_addr = exc_state.regs._fs.concat(exc_state.solver.BVV(0, 16))
        if exc_state.solver.is_true(exc_state.mem[tib_addr].long.resolved == -1):
            _l.debug("... no handlers registered")
            exception.args = ('Unhandled exception: %r' % exception,)
            raise exception
        # catch nested exceptions here with magic value在这里捕获具有魔术值的嵌套异常
        if exc_state.solver.is_true(exc_state.mem[tib_addr].long.resolved == 0xBADFACE):
            _l.debug("... nested exception")
            exception.args = ('Unhandled exception: %r' % exception,)
            raise exception

        # serialize the thread context and set up the exception record...序列化线程上下文并设置异常记录
        self._dump_regs(exc_state, exc_state.regs._esp - 0x300)
        exc_state.regs.esp -= 0x400
        record = exc_state.regs._esp + 0x20
        context = exc_state.regs._esp + 0x100
        # https://msdn.microsoft.com/en-us/library/windows/desktop/aa363082(v=vs.85).aspx
        exc_state.mem[record + 0x4].uint32_t = 0  # flags = continuable
        exc_state.mem[record + 0x8].uint32_t = 0  # FUCK chained exceptionsFUCK链式异常
        exc_state.mem[record + 0xc].uint32_t = exc_state.regs._eip  # exceptionaddress
        for i in range(16):  # zero out the arg count and args array将arg计数和args数组清零
            exc_state.mem[record + 0x10 + 4*i].uint32_t = 0
        # TOTAL SIZE: 0x50

        # the rest of the parameters have to be set per-exception type其余参数必须按例外类型设置
        # https://msdn.microsoft.com/en-us/library/cc704588.aspx
        if type(exception) is SimSegfaultException:
            exc_state.mem[record].uint32_t = 0xc0000005  # STATUS_ACCESS_VIOLATION
            exc_state.mem[record + 0x10].uint32_t = 2
            exc_state.mem[record + 0x14].uint32_t = 1 if exception.reason.startswith('write-') else 0
            exc_state.mem[record + 0x18].uint32_t = exception.addr
        elif type(exception) is SimZeroDivisionException:
            exc_state.mem[record].uint32_t = 0xC0000094  # STATUS_INTEGER_DIVIDE_BY_ZERO
            exc_state.mem[record + 0x10].uint32_t = 0

        # set up parameters to userland dispatcher 设置用户土地调度员的参数
        exc_state.mem[exc_state.regs._esp].uint32_t = 0xBADC0DE  # god help us if we return from this func 如果我们从这个功能中回来，上帝会帮助我们
        exc_state.mem[exc_state.regs._esp + 4].uint32_t = record # 这里是因为异常处理函数并不一定是按照ret指令返回的，有时需要其他的跳转指令来帮助返回原来的程序，使其正确运行
        exc_state.mem[exc_state.regs._esp + 8].uint32_t = context

        # let's go let's go!
        # we want to use a true guard here. if it's not true, then it's already been added in windup.我们想在这里使用一个真正的后卫。 如果不是真的，那么它已经在windup中被添加了
        successors.add_successor(exc_state, self._exception_handler, exc_state.solver.true, 'Ijk_Exception')
        successors.processed = True

    # these two methods load and store register state from a struct CONTEXT这两个方法从结构CONTEXT加载和存储寄存器状态
    # https://www.nirsoft.net/kernel_struct/vista/CONTEXT.html
