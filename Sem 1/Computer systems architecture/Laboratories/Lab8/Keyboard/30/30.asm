bits 32
global start

extern exit,scanf,printf
import exit msvcrt.dll
import scanf msvcrt.dll
import printf msvcrt.dll

segment data use32 class=data
    a dd 0
	b dd 0
	decimal_format db "%d",0
    final db '0'
    min_message db "Minimum number is: %d",0
segment code use32 class=code
start:
	push dword a
	push dword decimal_format
	call [scanf]
	add esp,4*2
    mov eax,[a]
    
    cmp eax,[b]
    jz final_message_write
    ;a=min
    while:
        push dword b
        push dword decimal_format
        call [scanf]
        add esp,4*2
        
        ;loop condition
        mov eax,[b]
        cmp eax,0
        jz final_message_write 
        ;-------

        cmp [a],eax
        jb while
        ;if a>b
            mov [a],eax
    jmp while
	
    final_message_write:
        push dword [a]
        push dword min_message
        call [printf]
        add esp,4*2

    push dword 0 
	call [exit] 