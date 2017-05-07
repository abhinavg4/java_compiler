section .text
	global scanInt0 
	global scanString0
	global printInt1
	global printString1
	extern printf
	extern scanf

SECTION .data
integer1 : times 4 db 0 ; 32-bits integer = 4 bytxes
formatin1: db "%d", 0
string1  : times 30 db 0
formatin2: db "%s", 0
char     : times 1 db 0

scanInt0:
        push integer1
        push formatin1 ; arguments are right to left (first parameter)
        call scanf
        add esp, 8
        mov eax, [integer1]
        pop ebx
        push eax
        push ebx
        ret

scanString0:
	push string1
	push formatin2
	call scanf
	add esp, 8
	mov eax, string1
	pop ebx
	push eax
	push ebx
	ret

scanString1:	
	mov eax, 3            ;sys_call number (sys_read)
        mov ebx, 0		  ;file descriptor (stdin)
        mov ecx, string1
        mov edx, 30
        int 0x80
	mov eax, string1
	ret

printString1:
	 mov eax, 4		  ;system call number (sys_write)
	 mov ebx, 1		  ;file descriptor (stdin)
	 mov ecx, [esp+4]
	 mov edx, 30	
	 int 0x80  
	 ret

printInt1:
	mov eax, [esp+4]
	xor esi, esi
	cmp eax, 0
	jge loop
	neg eax
	push eax
	mov eax, 45
	push eax
	mov eax, 4 ; Print '-'
	mov edx, 1
	mov ecx, esp
	mov ebx, 1
	int 0x80
	pop eax
	pop eax

loop:
	mov edx, 0
	mov ebx, 10
	div ebx
	add edx, 48
	push edx
	inc esi
	cmp eax, 0
	jz next
	jmp loop

next:
	cmp  esi, 0
	jz   exit
	dec  esi
	mov  eax, 4
	mov  ecx, esp
	mov  ebx, 1
	mov  edx, 1
	int  0x80
	add  esp, 4
	jmp  next

exit:
	call printNewLine
	ret

printNewLine:
        push ebp
	mov ebp, esp
	sub esp, 4

	; Print newline
	mov dword [ebp - 4], 0x0a
	mov eax, 4
	mov ebx, 1
	mov ecx, ebp
	sub ecx, 4
	mov edx, 1
	int 0x80

	mov esp, ebp
	pop ebp
	ret	
	 
