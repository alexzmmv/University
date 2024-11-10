bits 32 ;assembling for the 32 bits architecture
global start


;A string of words is given. Build two strings of bytes,
;s1 and s2, in the following way: for each word,

;if the no1( high byte)=no1( low byte)
;s1= no1(low byte)
;s2= 0

;if no1(high byte)>no1(low byte)
;s1= high byte 
;s2= low byte

;otherwise
;s1=low byte
;s2=high byte

extern exit
import exit msvcrt.dll
segment data use32 class=data

test_array dw 1100_1111_0000_1111b, 0101_0101_0101_0101b, 1111_0000_1111_0000b, 0011_1111_0000_1111b, 0
l_test equ ($-test_array)/2
resb 6
s1 resb 16
s2 resb 16

segment code use32 class=code
start:
	cld
    mov ecx,l_test
    mov esi,test_array
    xor edi,edi
    parse:
        mov ax,[esi]
        xor bx,bx
        ;clear bx
        ;bl=no1(lowbyte)
        ;bh=no1(highbyte)
        
        ;counting part
        lowcount:
            test al,1
            jz continue1
                inc bl
            continue1:
        shr al,1
        jnz lowcount
        
        highcount:
            test ah,1
            jz continue2
                inc bh
            continue2:
        shr ah,1
        jnz highcount
        ;counting part

        lodsw
        cmp bh,bl
        jz zero_case
        jg above_case

        ;below case:
            mov [s1+edi],al
            mov [s2+edi],ah
        jmp final_of_loop


        zero_case:
            mov [s1+edi],al
            mov [s2+edi],byte 0h
        jmp final_of_loop

        above_case:
            mov [s1+edi],ah
            mov [s2+edi],al
        jmp final_of_loop


    final_of_loop:
    inc edi
    loop parse

	push dword 0 
	call [exit]