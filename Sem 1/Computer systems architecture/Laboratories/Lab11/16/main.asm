bits 32
global start

%include "func.asm"

extern exit,scanf,fopen,fprintf,fclose 


import exit msvcrt.dll
import scanf msvcrt.dll
import fopen msvcrt.dll
import fprintf msvcrt.dll
import fclose msvcrt.dll



segment data use32 class=data
	number dd 0
	read_format db "%d",0
	file_descriptor dd -1
	file_name db "max.txt",0
	file_access db "w",0
	file_format db "%d"


segment code use32 class=code
start:
	xor ebx,ebx
	.while:
		call read_number
		call ebx_eax_max
		cmp eax,0h
	jne .while
	
	mov [number],ebx
	
	;open file 
	push dword file_access     
    push dword file_name
    call [fopen]
    add esp, 4*2
    mov [file_descriptor], eax


	;write to file
	push dword number
	push dword file_format
	push dword [file_descriptor]
	call [fprintf]
	add esp,4*3

	push dword [file_descriptor]
    call [fclose]
    add esp, 4


	push dword 0 
	call [exit] 