#!/usr/bin/env python3
#-*conding:utf-8-*-

# [XNiu2 16-Jul-2018]

import os
import re
import xlwings as xw

folderpath = os.path.dirname(os.path.abspath(__file__))
filename = 'in.xlsx'
fullpath = os.path.join(folderpath, filename)

wb = xw.Book(fullpath)
sht = wb.sheets.active
delete_mark = True

for i in range(2, 1192):
    lst = sht.range('A'+str(i)+':O'+str(i)).value
    if lst[0] == 2:
        delete_mark = False
    if lst[0] == 3:
        if re.search(r'Q2$', lst[4]):
            delete_mark = False
        else:
            delete_mark = True
    if delete_mark:
        sht.range('A'+str(i)+':O'+str(i)).clear()

for i in range(2, 1192):
    lst = sht.range('A'+str(i)+':O'+str(i)).value
    if lst[0] == 3:
        current_part_location = i
    if lst[0] == 4:
        if lst[2] == "Material Specification List":
            sht.range('O'+str(current_part_location)).value = lst[1]
        if re.match(r'NDE-11', str(lst[1])):
            sht.range('P'+str(current_part_location)).value = lst[1]
        if re.match(r'NDE-12', str(lst[1])):
            sht.range('Q'+str(current_part_location)).value = lst[1]
        if re.match(r'NDE-22', str(lst[1])):
            sht.range('R'+str(current_part_location)).value = lst[1]
        if re.match(r'NDE-31', str(lst[1])):
            sht.range('S'+str(current_part_location)).value = lst[1]
        if re.match(r'CIS-59', str(lst[1])):
            sht.range('T'+str(current_part_location)).value = lst[1]
