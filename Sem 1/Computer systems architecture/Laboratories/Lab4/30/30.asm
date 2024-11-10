bits 32 
global start

extern exit 
import exit msvcrt.dll  

segment data use32 class=data

a dw 010101010b
b dd 0h

segment code use32 class=code
start:
	mov ebx,[b]
	mov ax,[a]
	xor ax,0Ah
	mov cl,1
	shl ax,cl
	or bl,al
	;B(0-3)=A xor Ah(1-4)
	mov ax,[a]
	mov  cl,3
	shl ax,cl
	and ax,0FF0h
	or bx,ax
	;B(4-11)=A(7-14)
	mov eax,111111b
	mov cl,20
	shr eax,cl
	or ebx,eax
	;the bits 26-31 of C are the same as the bits 3-8 of A complemented
	;bits 3-8 complemented or A_complemented(3-8)
	push dword 0 
	call [exit] 