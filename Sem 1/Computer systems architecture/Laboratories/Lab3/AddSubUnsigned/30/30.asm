bits 32 
global start        

extern exit               
import exit msvcrt.dll    
                      
;(b+c+a)-(d+c+a)

segment data use32 class=data
    ; ...
    a db 0_FFh
    b dw 0_FF_FFh
    c dd 0_FF_FF_FF_FFh
    d dq 0FF_FFh
    aux dq 0
    
segment code use32 class=code
    start:
        mov eax,0
        mov ebx,0
        mov ecx,0
        mov edx,0
        
        mov eax,[c]
        mov [aux],eax
        mov eax,0
        mov bx,[b]
        mov eax,[c]
        add word[aux],bx
        adc dword[aux+2],0
        add dword[aux],eax
        adc dword[aux+4],0
        mov eax,0
        mov bx,0
        ;aux<-b+c+a
        clc
        mov eax,[c]
        add dword[d],eax
        adc dword[d+4],0h
        clc
        mov al,[a]
        add byte[d],al
        adc dword[d+1],0
        
        
        mov eax,[d]
        mov edx,[d+4]
        ;edx:eax<-d
        mov ebx,[aux]
        mov ecx,[aux+4]
        ;ecx:ebx<-aux
        clc
        adc eax,ebx
        adc edx,ecx
        
        ;the rezult is in EDX:EAX
        
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
