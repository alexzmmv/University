bits 32 ;assembling for the 32 bits architecture
global start

extern exit
import exit msvcrt.dll

segment data use32 class=data
    ;...
    A db 2,1,3,3,4,2,6
    lA dw $-A
    B db 4, 5, 7, 6, 2, 1
    lB dw $-B
    resb 1
    r resb 100
    ;...
segment code use32 class=code
start:
    mov ecx,0
    mov cx,[lB]
    mov esi,lB-1
    mov edi,0
    jcxz endBFor
    Bloop:
        mov al,[esi]
        mov [r+edi],al
        inc edi
        dec esi
    loop Bloop
    endBFor:
    
    mov ecx,0
    mov cx,[lA]
    mov esi,A
    jcxz endALoop
    Aloop:
        mov al,[esi]
        test al,1
        jz SfDaca
        ;if al is odd
            mov [r+edi],al
            inc edi
        SfDaca
        inc esi
    loop Aloop
    endALoop


	push dword 0
	call [exit] 