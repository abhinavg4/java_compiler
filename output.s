section .text
	global main

main:
	push ebp
	mov ebp , esp
	sub esp , 50
	mov ebx , 1
	pop ebp

	mov eax , 1
	mov ebx , 0
	int 0x80
