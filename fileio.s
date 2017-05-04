section .text
	global fcreate1
	global fwrite2
	global fclose1
	global fopen1
        global fread2

section	.data
file_name db "./file.txt" , 0
fd_out    : times 1 db 0
fd_in     : times 1 db 0
info      : times 26 db 0
msg	  : times 26 db 0

fcreate1:
	;create the file
	mov  eax, 8
	mov  ebx, file_name
	mov  ecx, 0777        ;read, write and execute by all
	int  0x80             ;call kernel
	ret

    ;call scanString0
    ;mov [msg], eax

fwrite2:
         ; write into the file
   mov	edx, 26          ;number of bytes
   mov	ecx, [esp+8]         ;message to write
   mov	ebx, [esp+4]    ;file descriptor 
   mov	eax,4            ;system call number (sys_write)
   int	0x80             ;call kernel
   ret	

fclose1:
; close the file
   mov eax, 6
   mov ebx, [esp+4]
   ret

fopen1:
    mov eax, 5
    mov ebx, file_name
    mov ecx, 0             ;for read only access
    mov edx, 0777          ;read, write and execute by all
    int  0x80
    ret

   ;mov  [fd_in], eax

fread2:
   ;read from file
   mov eax, 3
   mov ebx, [esp+4]
   mov ecx, info
   mov edx, 26
   int 0x80
    
   mov eax, 6
   mov ebx, [fd_in]
    
   ; print the info 
   mov eax, 4
   mov ebx, 1
   mov ecx, info
   mov edx, [esp+8]
   int 0x80
   ret

