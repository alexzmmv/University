bits 32 

global start        

extern exit               
import exit msvcrt.dll   

;(a*2)+2*(b-3)-d-2*c
; 24+10-27-30=
segment data use32 class=DATA
    rezult dd 0
    a db 12
    b db 8
    c db 15
    d dw 27

    
segment code use32 class=CODE
    start:
    
    mov eax,0
    mov ebx,0
    mov  ecx,0
    mov edx,0
    
    
    sub byte [b],3
    mov al,2
    mul byte [b]
    mov bx,ax
    ;bx<-2*(b-3)
    
    mov ax,2
    mul byte[c]
    mov cx,ax
    ;cx<- c*2
    
    
    mov ax,2
    mul byte[a]
    ;ax=2*a
    
    add eax,ebx
    sub eax,[d]
    sub eax,ecx
    
    mov [rezult],eax
    
       push    dword 0      
       call    [exit]  