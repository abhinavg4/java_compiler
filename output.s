section .text
	global main
	extern printInt1
	extern scanInt0
	extern printString1
	extern scanString0
	extern fcreate1
	extern fwrite2
	extern fclose1
	extern fopen1
	extern fread2
	extern append2
	extern val1
	extern next1

main:
	push ebp
	mov ebp , esp
	sub esp , 100
	push 1
	push 0
	call append2
	mov ebx , eax
	mov ecx , ebx
	mov esi , 0
	mov [ebp-12] , ebx
	mov [ebp-4] , ecx
	mov [ebp-8] , esi

label1:
	mov ebx , [ebp-8]
	cmp ebx , 5
	mov [ebp-8] , ebx
	jge label4
	jmp label3

label2:
	mov ebx , [ebp-8]
	mov ecx , ebx
	mov esi , ebx
	add esi , 1
	mov ebx , esi
	mov [ebp-8] , ebx
	jmp label1

label3:
	mov ebx , [ebp-8]
	mov ecx , ebx
	add ecx , 3
	push ecx
	mov esi , [ebp-12]
	push esi
	mov [ebp-8] , ebx
	mov [ebp-12] , esi
	call append2
	mov ebx , eax
	mov [ebp-12] , ebx
	jmp label2

label4:
	mov ebx , 0
	mov [ebp-8] , ebx

label5:
	mov ebx , [ebp-8]
	cmp ebx , 5
	mov [ebp-8] , ebx
	jge label10
	jmp label7

label6:
	mov ebx , [ebp-8]
	mov ecx , ebx
	mov esi , ebx
	add esi , 1
	mov ebx , esi
	mov [ebp-8] , ebx
	jmp label5

label7:
	mov ebx , [ebp-4]
	push ebx
	mov [ebp-4] , ebx
	call val1
	mov ebx , eax
	cmp ebx , 5
	mov [ebp-16] , ebx
	jne label9
	jmp label8

label8:
	push 1
	call printInt1

label9:
	mov ebx , [ebp-4]
	push ebx
	mov [ebp-4] , ebx
	call next1
	mov ebx , eax
	mov [ebp-4] , ebx
	jmp label6

label10:

	mov eax , 1
	mov ebx , 0
	int 0x80
