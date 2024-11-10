bits 32 

global start        

extern exit               
import exit msvcrt.dll   

;[(a-b)*5+d]-2*c
;[(12-8)*5+27]-2*15
;(4*5+27)-30
;47-30=17
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
    
    mov al,[a]
    sub ax,word[b]
    mov cl,5h
    mul byte cl
    mov bx,ax
    ;bx<-(a-b)*5
    mov ax,2
    mul byte[c]
    ;ax<-2*c
    add bx,[d]
    ;bx<-[(a-b)*5+d]
    sub bx,ax
    ;bx<-[(a-b)*5+d]-2*c
    
    
    mov [rezult],bx
    
       push    dword 0      
       call    [exit]  