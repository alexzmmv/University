bits 32 
global start        

extern exit               
import exit msvcrt.dll    
                      
;c+a+b+b+a
segment data use32 class=data
    ; ...
    a db 0_FFh
    b dw 0_FF_FFh
    c dd 0F_FF_FF_FFh
    d dq 0FF_FFh
    aux dq 0
    
segment code use32 class=code
    start:
        mov eax,0
        mov ebx,0
        mov ecx,0
        mov edx,0
        
        mov ecx,[c]
        mov al,[a]
        cbw
        cwd
        push dx
        push ax
        pop eax
        add ecx,eax
        mov eax,0
        mov ax,[b]
        cwd
        push dx
        push ax
        pop eax
        add ecx,eax
        add ecx,eax
        
        mov dx,0
        mov ax,0
        mov al,[a]
        cbw
        cwd
        push dx
        push ax
        pop eax
        add ecx,eax
        
        ;rezult is in ecx
        
        
        
        
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
