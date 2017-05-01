section .text
	global main

anuj1:
	push ebp
	mov ebp , esp
	sub esp , 50
	mov ecx , [ebp-4]
	mov ebx , ecx
	add ecx , 5
	mov [ebp-4] , ecx
	pop ebp
	ret

abhi2:
	push ebp
	mov ebp , esp
	sub esp , 50
	mov ebx , [ebp--8]
	mov esi , ebx
	add ebx , 10
	mov [ebp+8] , ebx
	pop ebp
	ret

main:
	push ebp
	mov ebp , esp
	sub esp , 50
	mov eax , 5
	mov ebx , [ebp--8]
	mov eax , ebx
	add ebx , 4
	call abhi2
	pop ebp
	ret

	mov eax , 1
	mov ebx , 0
	int 0x80
