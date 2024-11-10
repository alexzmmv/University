bits 32 ;assembling for the 32 bits architecture
global start

extern exit
import exit msvcrt.dll
segment data use32 class=data

 s DD 12345607h, 1A2B3C15h
 s_len equ ($-s)/4
 resq 1
 d resb s_len*4
 d_len equ s_len*4

segment code use32 class=code
start:
	mov esi,s
	mov edi,d
	mov ecx,d_len
	cld
	rep movsb

	xor ecx,ecx
.outer_loop:
    mov esi, ecx                
    mov ebx, ecx            

.inner_loop:
    ; Compare s[esi] with s[ebx] (minimum)
    mov al, [d + esi]
    cmp al, [d + ebx]
    jbe smaller           ; if s[esi] <= s[ebx], jump to smaller
    mov ebx, esi          ; update minimum index

smaller:
    inc esi               ; move to the next element
    cmp esi, d_len        ; check if we reached the end of the array
    jb .inner_loop         ; if not, continue the inner loop

    ;Swap s[ecx] and s[ebx]
    mov al, [d + ecx]
    mov ah, [d + ebx]
    mov [d + ecx], ah
    mov [d + ebx], al

    inc ecx
    cmp ecx, d_len              ; check if we reached the end of the array
    jb .outer_loop               ; if not, continue the outer loop

	push dword 0 
	call [exit]