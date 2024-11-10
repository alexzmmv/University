bits 32

global start

extern exit,fopen,fprintf,fclose,scanf
import exit msvcrt.dll
import fopen msvcrt.dll
import scanf msvcrt.dll
import fclose msvcrt.dll
import fprintf msvcrt.dll

segment data use32 class=data
    filename db 'output.txt', 0
    mode db 'w', 0 ; write mode
    input_format db '%s', 0
    output_format db '%s', 0
    word_ resb 100
    stop_char db '$', 0
    file dd 0 ; file descriptor
    newline db 10, 0
segment code use32 class=code
start:
    ; create file
    push mode
    push filename
    call [fopen]
    add esp, 8 ; clean up the stack
    mov [file], eax ; store the file descriptor

    
    ;verify if word contains at least one digit
    ;if yes, write it to file
    ;else, read another word
    
    while:
        push dword word_
        push dword input_format
        call [scanf]
        add esp, 8 ; clean up the stack
        
        mov al,[word_]
        cmp al,[stop_char]
        je end

        mov esi,word_
        iterate_word:
            mov al,[esi]
            cmp al,0
            je end_iterate_word
            cmp al,'0'
            jb next_letter
            cmp al,'9'
            ja next_letter

            ;write word to file
            push dword word_
            push dword [file]
            call [fprintf]
            add esp, 8 ; clean up the stack
            push dword newline
            push dword [file]
            call [fprintf]
            add esp, 8 ; clean up the stack
            
            jmp end_iterate_word

            next_letter:
            inc esi
            jmp iterate_word
        end_iterate_word:
    
    jmp while 

    end:
    ; close file
    push dword [file]
    call [fclose] 
    ; exit
    push dword 0 
    call [exit] 


    