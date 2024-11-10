bits 32
global start

extern exit,printf,scanf
import exit msvcrt.dll
import printf msvcrt.dll
import scanf msvcrt.dll

segment data use32 class=data
	a dd 0
	b dd 0
	a_eq db "a=",0
	b_eq db "b=",0
	decimal_format db "%d",0
	hexa_format db "a+b=%x",0
	
segment code use32 class=code
start:
	push dword a_eq
	call [printf]
	add esp,4*1

	push dword a
	push dword decimal_format
	call [scanf]
	add esp,4*2

	push dword b_eq
	call [printf]
	add esp,4*1

	push dword b
	push dword decimal_format
	call [scanf]
	add esp,4*2

	mov eax,[a]
	add eax,[b]

	push dword eax
	push dword hexa_format
	call[printf]
	add esp,4*2
	push dword 0 
	call [exit] 