bits 32 
global start        

extern exit               
import exit msvcrt.dll    
          
;a*b-(100-c)/(b*b)+e+x; a-word; b,c-byte; e-doubleword; x-qword
segment data use32 class=data
    ; ...
    a db 0ah
    b db 19h
    c db 0Fh
    e dd 0FF_FFh
    x dq 0FA124584h
    
segment code use32 class=code
    start:
        mov eax,0
        mov ebx,0
        mov ecx,0
        mov edx,0
        
        mov al,[b]
        imul al
        mov cx,ax
        ;cx<-b*b
        
        mov al,[c]
        cbw
        cwd
        clc
        sub ax,100
        sbb dx,0
        ;dx:cx<-100-c
        
        idiv cx
        mov dx,0
        cwde
        mov ecx,eax
        ;ecx<-(100-c)/(b*b)
        
        mov al,[b]
        cbw
        imul word[a]
        push dx
        push ax
        pop eax
        ;eax<-a*b
        
        sub eax,ecx
        add eax,[e]
        mov edx,0
        ;edx:eax<-a*b-(100-c)/(b*b)+e
        
        mov ebx, dword [x+0] 
        mov ecx, dword [x+4] 
        ;ecx:ebx<-x
        clc  
        add eax, ebx   
        adc edx, ecx         
        
        ;rezult is in edx:eax
        
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
