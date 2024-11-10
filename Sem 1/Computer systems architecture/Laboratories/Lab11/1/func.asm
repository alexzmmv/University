%ifndef _FUNC_ASM_ ; if FILE is not defined
%define _FUNC_ASM_ ; then we define it


_pereaxnext:
    ror eax, 4
    ret

%endif ; end of _FUNC_ASM_ definition