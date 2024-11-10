bits 32 

global start        

extern exit               
import exit msvcrt.dll   

; 100/(e+h-3*a)

segment data use32 class=data
    q_ dd 0
    
    blank db 0FFh
    
    reminder_ dd 0 
    
    blank2 db 0FFh
    a db 12
    b db 8
    c db 15
    d db 0BBh
    e dw 0FF2h
    f dw 0AF8h
    g dw 0EFBh
    h dw 0BF2h
    
segment code use32 class=code
    start:
    
    mov eax,0
    mov ebx,0
    mov  ecx,0
    mov edx,0
    
    mov ebx,e
    mov ecx,h
    add ecx,ebx
    mov al,3
    mul byte[a]
    mov ebx,0
    mov bx,ax
    
    mov edx,0
    mov eax,100d
    
    div ebx
    
    mov [q_],eax
    mov [reminder_],edx
    
   
     
     
       push    dword 0      
       call    [exit]  