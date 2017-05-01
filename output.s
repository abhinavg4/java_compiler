section .text
	global main

abhi1:
	push ebp
	mov ebp , esp
	sub esp , 50
	mov ebx , [ebp+8]
	cmp ebx , 15
	jle label2
	jmp label1

label1:
	mov eax , [ebp+8]
	mov esp , ebp
	pop ebp
	ret

label2:
	mov ebx , [ebp+8]
	mov ecx , ebx
	add ecx , 5
	push ecx
	mov [ebp+8] , ebx
	mov [ebp-4] , ecx
	call abhi1
	mov eax , [ebp+8]
	mov esp , ebp
	pop ebp
	ret

main:
	push ebp
	mov ebp , esp
	sub esp , 50
	mov ebx , 5
	push 5
	mov [ebp-4] , ebx
	call abhi1
	pop ebp

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
