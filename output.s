section .text
	global main

fact1:
	push ebp
	mov ebp , esp
	sub esp , 50
	mov ebx , 1
	mov ecx , [ebp+8]
	cmp ecx , 1
	mov [ebp-4] , ebx
	mov [ebp+8] , ecx
	jne label2
	jmp label1

label1:
	mov eax , [ebp-4]
	mov esp , ebp
	pop ebp
	ret

label2:
	mov ebx , [ebp+8]
	mov ecx , ebx
	sub ecx , 1
	push ecx
	mov [ebp+8] , ebx
	call fact1
	mov ebx , eax
	mov edx , ebx
	mov eax , [ebp+8]
	imul edx
	mov esp , ebp
	pop ebp
	ret

main:
	push ebp
	mov ebp , esp
	sub esp , 50
	push 5
	call fact1

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
