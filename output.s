section .text
	global main

Ack2:
	push ebp
	mov ebp , esp
	sub esp , 50
	mov ebx , [ebp+8]
	cmp ebx , 0
	jl label9
	jmp label1

label1:
	mov ecx , [ebp+12]
	cmp ecx , 0
	jl label9
	jmp label2

label2:
	cmp ebx , 0
	jne label5
	jmp label3

label3:
	mov esi , ecx
	add esi , 1
	jmp label4

label5:
	cmp ecx , 0
	jne label8
	jmp label6

label6:
	mov edi , ebx
	sub edi , 1
	push 1
	push edi
	mov [ebp+8] , ebx
	mov [ebp+12] , ecx
	mov [ebp-4] , esi
	call Ack2
	jmp label7

label8:
	mov ebx , [ebp+8]
	mov ecx , ebx
	sub ecx , 1
	mov esi , [ebp+12]
	mov edi , esi
	sub edi , 1
	push edi
	push ebx
	mov [ebp+8] , ebx
	mov [ebp-8] , ecx
	mov [ebp+12] , esi
	mov [ebp-4] , eax
	call Ack2
	push eax
	mov ebx , [ebp-8]
	push ebx
	mov [ebp-8] , ebx
	call Ack2

label7:

label4:

label9:
	mov eax , [ebp-4]
	mov esp , ebp
	pop ebp
	ret

main:
	push ebp
	mov ebp , esp
	sub esp , 50
	push 2
	push 1
	call Ack2
	mov eax , 5

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
