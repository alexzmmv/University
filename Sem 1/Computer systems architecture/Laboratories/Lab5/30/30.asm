bits 32 ;assembling for the 32 bits architecture
global start

extern exit
import exit msvcrt.dll

segment data use32 class=data
    ;...
    A db 1, 3, 6, 2, 3, 2
    lA dw $-A
    B db 6, 3, 8, 1, 2, 5
    lB dw $-B
    r resw 100
    ;...
segment code use32 class=code
start:
    mov ecx,0
    mov cx,[lA]
    mov esi,0
    mov edi,0
    jecxz final
    forstrings:
        mov ax,0
        mov bx,0
        mov al,[A+esi]
        mov bl,[B+esi]
        add ax,bx
        mov [r+edi],ax
        add edi,2
        inc esi
    loop forstrings
    final:

	push dword 0
	call [exit] 