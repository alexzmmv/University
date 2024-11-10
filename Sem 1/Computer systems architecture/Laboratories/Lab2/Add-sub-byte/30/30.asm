bits 32 

global start        

extern exit               
import exit msvcrt.dll     

;d-(a+b)-(c+c)
;27-(12+8)-(15+15)
;27-20-30

segment data use32 class=DATA
    
    a db 12
    b db 8
    c db 15
    d db 27
    
segment code use32 class=CODE
    start:
    
    mov eax,0
    mov ebx,0
    mov ecx,0
    mov edx,0
    mov al, [a]
    mov bl, [b]
    mov cl, [c]
    mov dl, [d]

   add ax,bx
   add cx,cx
   sub dx,ax
   sub dx,cx
   mov ax,dx
   
   
        push    dword 0      
        call    [exit]  
        
;