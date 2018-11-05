#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# [XNiu2 06-Feb-2018]

import xlwings as xw
import os
import re
import csv

with open('origin.csv', 'r', newline='') as header:
    with open('table.csv', 'w', newline='') as tables:
        head = header.readlines()
        base = re.findall(r'\d{9}', head[0])
        for line in head[3:]:
            tables.write(line)

with open('table.csv', 'r', newline='') as csvfile:
    with open('EBOM.csv', 'w', newline='') as ebomfile:
        reader = csv.DictReader(csvfile)
        id_group = [0,0,0,0,0]
        head = reader.fieldnames
        head[-1] = 'parent_name'
        # print (head)
        writer = csv.DictWriter(ebomfile, head) 
        writer.writeheader()
        for row in reader:
            id_group[int(row['Level'])-1] = row['Name']
            try:
                row['parent_name'] = id_group[int(row['Level'])-2]
            except:
                row['parent_name'] = 'NA'
            # print (row)
            writer.writerow(row)
        
