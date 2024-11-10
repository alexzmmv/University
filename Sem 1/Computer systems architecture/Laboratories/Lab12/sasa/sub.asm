bits 32
global _rotate
segment data public data use32
segment code public code use32

;rotate(int a)
_rotate:
	push ebp
    mov ebp, esp
    
    mov eax, [ebp + 8];eax= a     
    
    ror eax, 4;eax= a>>4 
    
    mov esp, ebp
    pop ebp

    ret;eax is returned