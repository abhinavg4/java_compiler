section .text
	global append2

append2:
  push ebp
  mov ebp , esp
  sub esp, 20

  mov eax , [ebp+8]
  cmp eax,0
  jne label1

  mov eax , 45
  xor ebx , ebx
  int 0x80
	jmp label2

label1:

  add eax , 8
  mov ebx, eax
  mov eax, 45
  int 0x80

  mov edx , [ebp+8]
  mov [edx] , eax
  mov ebx, [ebp+12]
  mov [edx+4],ebx

label2:
  mov esp, ebp
  pop ebp
  ret
