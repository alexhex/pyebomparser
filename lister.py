#!usr/bin/python3
#-*-coding:utf-8-*-
# [XNiu2 2018-11-16]

import re
import csv
import os


class Converter:
    def __init__(self):
        self.table = []
    
    def head_make(self, path):
        with open(path, 'r', newline='') as header:
            head = header.readlines()
            for i in range(len(head)):
                if re.match(r'Level,', head[i]):
                    break
                return None
        self.table = head[i:]

class Rule:
    def __init__(self):
        self.type = ''

    def action(self, ) 
    
class Ebom:
    def __init__(self):
        self.ebom = []
        self.ebom_depth = 0
    
    def table_make(self, Converter):
        lines = list(csv.DictReader(table))
        id_group = [0] * 5
        for row in lines:
            id_group[int(row['Level'])-1] = row['Name']
            try:
                row['Parent Name'] = id_group[int(row['Level'])-2]
            except:
                row['Parent Name'] = 'NA'

            try:
                row['Qty'] = float(re.sub(r'[=\"\']','', row['Qty'])) 
            except:
                row['Qty'] = ''
            try:
                x = row['Item Number']
                x = int(re.sub(r'\D','',x))
                row['Item Number'] = x 
            except:
                row['Item Number'] = ''
            # print (row)
        self.ebom = lines


class Rule:
    def change(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
        if callable(method): return method(*args)

    def convert(self, name):
        self.change('convert_', name)
    

class QtyRule(Rule):
    def change_qty(self, value):
        return float(re.sub(r'[^\d\.]', '', value)) 

class ItemNumberRule(Rule):
    def change_item_number(self, value):
        return int(re.sub(r'\D', '', value))



baseebom = EbomTable()
baseebom.
