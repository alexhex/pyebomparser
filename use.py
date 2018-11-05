#!/usr/bin/env python3
#-*conding:utf-8-*-

import os
import re

folderpath = os.path.dirname(os.path.abspath(__file__))
filename = "in.txt"
filepath = os.path.join(folderpath, filename)

filename2 = "out.txt"
filepath2 = os.path.join(folderpath, filename2)

str_in = open(filepath, 'r') 
str_out = open(filepath2, 'w')
line = '1'

while(line):
    line = str_in.readline()
    print (line)
    matchobj = re.match(r'[0-9].*:.*', line)
    if matchobj:
        print ("YES")
        str_out.write(line)

str_in.close()
str_out.close()
