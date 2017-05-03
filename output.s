section .text
	global main
	extern printInt1

main:
	push ebp
	mov ebp , esp
	sub esp , 50
	mov ebx , 5
	mov ecx , ebx
	add ecx , 1
	push ecx
	mov [ebp-4] , ecx
	call printInt1
	mov ebx , 5
	mov ecx , ebx
	mov eax , ebx
	add eax , 1
	push ecx
	mov [ebp-4] , eax
	call printInt1
	mov ebx , 5
	mov eax , ebx
	sub eax , 1
	push eax
	mov [ebp-4] , ebx
	call printInt1
	mov ebx , -5
	mov ecx , ebx
	sub ecx , 10
	push ecx
	mov [ebp-4] , ebx
	call printInt1

	mov eax , 1
	mov ebx , 0
	int 0x80
