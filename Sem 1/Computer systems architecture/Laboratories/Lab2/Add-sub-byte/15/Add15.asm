bits 32 

global start        

extern exit               
import exit msvcrt.dll     

;a-b-d+2+c+(10-b)
;12-8-27+2+15+(10-8)=-4

segment data use32 class=DATA
#
    
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

   
    sub ax, bx    ; a - b
    sub ax, dx    ; a - b - d
    add ax, word 2     ; a - b - d + 2
    add ax, cx    ; a - b - d + 2 + c
    neg bx    ; 10 - b
    add bx,10
    add ax, bx    ; a - b - d + 2 + c + (10 - b)
        
        push    dword 0      
        call    [exit]  
        
;