### This code use ctypes to generate c like random number
### and use pwntools to accesss particular array elements here "check" array read each element as 32 bit integer
### performing some operations


import ctypes
libc = ctypes.CDLL('libc.so.6')
mapping = {}
for i in range(255):
    libc.srand(i)
    mapping[libc.rand()] = chr(i)
flag = ""
from pwn import *
casino = ELF("./casino", checksec=False)
for b in range(29):
    val = casino.u32(casino.sym["check"] + b * 4)
    flag += mapping[val]
print(flag)