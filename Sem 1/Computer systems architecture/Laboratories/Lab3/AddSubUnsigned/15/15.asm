bits 32 
global start        

extern exit               
import exit msvcrt.dll    
                      
;a+b-c+(d-a)

segment data use32 class=data
    ; ...
    a db 0FFh
    b dw 0FFFFh
    c dd 2345h
    d dq 12_1B_12_12_8Ah
    ; ...
segment code use32 class=code
    start:
        mov eax,0
        mov ebx,0
        mov ecx,0
        mov edx,0
        
        mov al,[a]
        mov bx,[b]
        add bx,ax
        ;bx<a+b
        mov eax,[c]
        sub ebx,eax
        ;ebx<-a+b-c
        mov al,[a]
        sub dword [d+0],eax
        sbb dword [d+4],0h
        ;d<-d-a
        add dword [d+4],ebx
        adc dword [d+0],0h
        ;d<-
        ;the rezult is in d location memory
        
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
