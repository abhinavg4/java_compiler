section .text
	global next1

next1:
  push ebp
  mov ebp , esp
  sub esp, 20

  mov ebx , [ebp+8]
  mov eax , [ebx]

  mov esp, ebp
  pop ebp
  ret
