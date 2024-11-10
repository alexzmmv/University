%ifndef _FUNC_ASM_ ; if FILE is not defined
%define _FUNC_ASM_ ; then we define it

ebx_eax_max:
	;unsigned ebx - max(eax,ebx)
	cmp eax,ebx
	ja .end
	mov ebx,eax
	.end:
	ret

read_number:
	pushad
	push dword number
	push dword read_format
	call [scanf]
	add esp,4*2
    popad
    mov eax,[number]
	ret

%endif ; end of _FUNC_ASM_ definition