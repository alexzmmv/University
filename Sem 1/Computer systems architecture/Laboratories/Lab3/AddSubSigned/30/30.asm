bits 32 
global start        

extern exit               
import exit msvcrt.dll    
          
;d-a+c+c-b+a

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
        
        mov ecx,[d+4]
        mov ebx,[d]
        ;ecx:ebx<-d
        mov al,[a]
        cbw
        cwde
        cdq
        clc
        sub ebx,eax
        sbb ecx,edx
        ;d-a
        mov edx,0
        mov eax,[c]
        cwde
        add ebx,eax
        adc ecx,edx
        add ebx,eax
        adc ecx,edx
        ;d-a+c+c
        mov ax,[b]
        cwde
        cdq
        clc
        sub ebx,eax
        sbb ecx,edx
        
        mov al,[a]
        cbw
        cwd
        push dx
        push ax
        pop eax
        cwde
        clc
        add ebx,eax
        adc ecx,edx

        ;rezult is in ecx:ebx
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
