import os

with open("copyright_header.txt", "r") as fd:
	header = fd.read()

path = "../source/nordic_sdk"
for root, dirs, files in os.walk(path):
	for fn in [os.path.join(root, x) for x in files]:
		with open(fn, "r+") as fd:
			print "+"*35
			print fn
			s = fd.read()
			start = s.find("/*")
			end = s.find("*/")
			copyright_str = s[start:end+2]
			if "copyright (c)" not in copyright_str.lower():
				s = header + "\n\n" + s
			elif copyright_str is not header:
				s = s.replace(copyright_str, header)

			fd.seek(0)
			fd.write(s)
			fd.truncate()
