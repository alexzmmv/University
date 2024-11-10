bits 32
global start
 
extern exit
import exit msvcrt.dll

segment data use32 class=data

a dw _1101_11101000001b
b dw 11_101101_0b
c dd 0

segment code use32 class=code
start:
	mov ebx,[c]
	mov eax,0
	or ebx,111000b
	;3-5=1
	mov ax,[a]
	mov cl,5
	shr ax,cl
	and ax,111000000b
	or ebx,eax
	; C(6-9)=A(11-14)
	mov eax,0
	mov ax,[b]
	and ax,1111110b
	mov cl,10
	shl eax,cl
	or ebx,eax
	;C(10-15)=B(1-6)
	mov eax,0FFFFh
	mov cl,16
	shl eax,cl
	or ebx,eax
	;C(16-31)=1
	mov ebx,c

	push dword 0
    call [exit] 