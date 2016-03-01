#!/usr/bin/env python
# Copyright (C) 2012 by Kirik Konstantin <snegovick>

import qrencode
import sys

f = open(sys.argv[1], "r")
for i, l in enumerate(f.readlines()):
    version, size, image = qrencode.encode_scaled(l.replace("\n", ""), 1024)
    print "version:", version, "size:", size
    f_out = open(str(i)+".png", "w")
    image.save(f_out, "PNG")
    f_out.close()

f.close()
