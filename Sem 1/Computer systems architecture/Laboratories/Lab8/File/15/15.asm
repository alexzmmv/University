bits 32
global start

extern exit,fopen,fprintf,fclose
import exit msvcrt.dll
import fopen msvcrt.dll
import fclose msvcrt.dll
import fprintf msvcrt.dll

segment data use32 class=data
	file_name db "file.txt",0
	acces_mode db 'w',0
	file_descriptor resd 1
	text db "Hello! This is a test text with 123 and special characters #$%",0
	output_text db $-text-1
				db 0

segment code use32 class=code
start:
	; Replace special characters with 'X'
		lea esi, [text]
		lea edi, [output_text]
		mov ecx, 0

	replace_special_chars:
		mov al, [esi + ecx]
		cmp al, 0
		je  write_to_file

		cmp al,' '
		je not_special_char
		cmp al, '0'
		jb  is_special_char
		cmp al, '9'
		jbe not_special_char
		cmp al, 'A'
		jb  is_special_char
		cmp al, 'Z'
		jbe not_special_char
		cmp al, 'a'
		jb  is_special_char
		cmp al, 'z'
		jbe not_special_char

	not_special_char:
		mov [edi + ecx], al
		jmp continue_loop

	is_special_char:
		mov byte [edi + ecx], 'X'

	continue_loop:
		inc ecx
		jmp replace_special_chars

	write_to_file:
		push dword acces_mode
		push dword file_name
		call[fopen]
		add esp,4*2
		mov [file_descriptor],eax

		cmp eax,0
		je final
		push dword output_text
		push dword [file_descriptor]
		call [fprintf]
		add esp,4*2

		push dword [file_descriptor]
		call [fclose]
		add esp,4


	final:
	push dword 0 
	call [exit] 