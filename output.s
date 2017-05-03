section .text
	global main
	extern printInt1

main:
	push ebp
	mov ebp , esp
	sub esp , 100
	mov eax , 0
	mov edx , 8
	imul edx
	mov ebx , eax
	mov eax , 0
	mov edx , 4
	imul edx
	mov ecx , ebx
	add ecx , eax
	mov ebx , 1
	add ecx , ebp
	sub ecx , 28
	mov [ecx] , ebx
	mov eax , 0
	mov edx , 8
	imul edx
	mov ebx , eax
	mov eax , 1
	mov edx , 4
	imul edx
	mov ecx , ebx
	add ecx , eax
	mov ebx , 2
	add ecx , ebp
	sub ecx , 28
	mov [ecx] , ebx
	mov eax , 1
	mov edx , 8
	imul edx
	mov ebx , eax
	mov eax , 0
	mov edx , 4
	imul edx
	mov ecx , ebx
	add ecx , eax
	mov ebx , 3
	add ecx , ebp
	sub ecx , 28
	mov [ecx] , ebx
	mov eax , 1
	mov edx , 8
	imul edx
	mov ebx , eax
	mov eax , 1
	mov edx , 4
	imul edx
	mov ecx , ebx
	add ecx , eax
	mov ebx , 4
	add ecx , ebp
	sub ecx , 28
	mov [ecx] , ebx
	mov eax , 0
	mov edx , 8
	imul edx
	mov ebx , eax
	mov eax , 0
	mov edx , 4
	imul edx
	mov ecx , ebx
	add ecx , eax
	mov ebx , 5
	add ecx , ebp
	sub ecx , 44
	mov [ecx] , ebx
	mov eax , 0
	mov edx , 8
	imul edx
	mov ebx , eax
	mov eax , 1
	mov edx , 4
	imul edx
	mov ecx , ebx
	add ecx , eax
	mov ebx , 6
	add ecx , ebp
	sub ecx , 44
	mov [ecx] , ebx
	mov eax , 1
	mov edx , 8
	imul edx
	mov ebx , eax
	mov eax , 0
	mov edx , 4
	imul edx
	mov ecx , ebx
	add ecx , eax
	mov ebx , 7
	add ecx , ebp
	sub ecx , 44
	mov [ecx] , ebx
	mov eax , 1
	mov edx , 8
	imul edx
	mov ebx , eax
	mov eax , 1
	mov edx , 4
	imul edx
	mov ecx , ebx
	add ecx , eax
	mov ebx , 8
	add ecx , ebp
	sub ecx , 44
	mov [ecx] , ebx
> /home/abhigarg/bitbucket/java_compiler/src/regalloc.py(236)regs()
-> regalloc[a] = var
(Pdb) 