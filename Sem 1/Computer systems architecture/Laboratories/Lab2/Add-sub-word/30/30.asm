bits 32 


global start        

extern exit               
import exit msvcrt.dll     

;a-b+(c-d+a)
;12-8+(15-27+12)
;4+0=0

segment data use32 class=DATA
    rezult dd 0
    a dw 12
    b dw 8
    c dw 15
    d dw 27
    
segment code use32 class=CODE
    start:
    
    mov eax,0
    mov ebx,0
    mov ecx,0
    mov edx,0
    mov ax, [a]
    mov bx, [b]
    mov cx, [c]
    mov dx, [d]
    sub eax,ebx
    
    mov bx,[a] 
    sub ecx,edx
    add ecx,ebx
    
    add eax,ecx
    
    mov [rezult],eax
    
       push    dword 0      
       call    [exit]  