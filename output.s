section .text
	global main

anuj1:
	push ebp
	mov ebp , esp
	sub esp , 50
	mov ebx , [ebp-4]
	mov [ebp+8] , ebx
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
	mov ebx , [ebp+8]
	mov esi , ebx
	add ebx , 10
	mov [ebp+8] , eax
	pop ebp
	ret

main:
	push ebp
	mov ebp , esp
	sub esp , 50
	mov edx , 5
	mov ebx , [ebp+12]
	mov edx , ebx
	add ebx , 4
	call abhi2
	pop ebp
	ret

	mov eax , 1
	mov ebx , 0
	int 0x80

printInt:
	mov eax, [esp+8]
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
	ret
