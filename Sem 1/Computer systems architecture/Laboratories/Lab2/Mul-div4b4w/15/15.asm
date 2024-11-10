bits 32 

global start        

extern exit               
import exit msvcrt.dll   

; f*(e-2)/[3*(d-5)]
;
segment data use32 class=data
    q_ dd 0
    
    blank db 0FFh
    
    reminder_ dd 0 
    
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
    
    sub byte [d],5h;d<-d-5
    mov al,3
    mul byte[d];ax<-[3*(d-5)]
    mov ebx,eax
    ;bx<-[3*(d-5)]
    
    mov dx,0
    sub word[e],2;e<-e-2
    mov ax,[e]
    mul word [f]
    ;dx:ax<- f*(e-2)
    
    div bx
    ;ax<-f*(e-2)/[3*(d-5)] quotient
    ;dx<-f*(e-2)/[3*(d-5)] reminder
    
    mov [q_],eax
    mov [reminder_],edx
     
     
       push    dword 0      
       call    [exit]  