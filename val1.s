section .text
	global val1

val1:
  push ebp
  mov ebp , esp
  sub esp, 20

  mov ebx , [ebp+8]
  mov eax , [ebx+4]
  
  mov esp, ebp
  pop ebp
  ret
