bits 32 
global start        

extern exit               
import exit msvcrt.dll    
          
;x-(a*b*25+c*3)/(a+b)+e; a,b,c-byte; e-doubleword
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
        
        mov al,[a]
        cbw
        mov bx,ax
        mov ax,0
        mov al,[b]
        cbw
        add bx,ax
        mov ax,0
        ;bx<-a+b
        
        mov al,[c]
        mov ah,4
        imul ah
        mov cx,ax
        ;cx<-c*3
        
        mov al,[a]
        imul byte[b]
        mov dx,25d
        imul dx
        ;dx:ax<-a*b*25
        
        clc
        add ax,cx
        adc dx,0
        ;dx:ax<-a*b*25+c*3
        
        idiv bx 
        cwde
        cdq
        ;edx:eax<-(a*b*25+c*3)/(a+b)
        
        mov ecx,[x+4]
        mov ebx,[x]
        
        clc
        sub ebx,eax
        sbb ecx,edx
        
        mov eax,[e] 
        clc
        add ebx,eax
        add ecx,0
        
        ;rezult  is is ecx:ebx
        
        
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
