bits 32
global start

extern exit, printf
import exit msvcrt.dll
import printf msvcrt.dll


%include "func.asm"

segment data use32 class=data
    a dd 210F342h
    hexaformat db "%x", 10, 0
segment code use32 class=code


print:
    pushad
    
    push eax
    push hexaformat
    call [printf]
    add esp, 8
    
    popad
    ret 


start:
    mov ecx, 8h

    mov eax, [a]
    .for:
    
        call print
        
        call pereaxnext
        
    loop .for    ; Decrement ecx and repeat the loop if ecx is not zero

    push 0
    call [exit]