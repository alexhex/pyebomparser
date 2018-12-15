#!usr/bin/python3
#-*-coding:utf-8-*-

import os
import re
import csv
# import collections

class RawTable:
    def __init__(self):
        self.table = []
    
    def make_table(self, path):
        with open(path, 'r', newline='') as header:
            head = header.readlines()
            for i in range(len(head)):
                if re.match(r'Level,', head[i]):
                    break
            self.table = head[i:]
            # print (self.table)
    
    def return_table(self):
        return self.table if self.table else None


class ValConverter:
    def convert(self, typ, *args):
        func_name = 'convert_' + '_'.join(typ.lower().split(' '))
        method = getattr(self, func_name, None)
        if hasattr(method, '__call__'): return method(*args)
        # if isinstance(method, collections.Callable): return method(*args)
    
    def convert_qty(self, val):
        return float(re.sub(r'[=\"\']', '', val)) if val else 0
    
    def convert_item_number(self, val):
        return int(re.sub(r'\D', '', val)) if val else 0
    
    def convert_level(self, val):
        return int(re.sub(r'\D', '', val)) if val else 0


class Ebom:
    def __init__(self, table, converter):
        self.ebom = {}
        self.ebom_depth = 0
        self.rawtable = table.return_table()
        self.converter = converter

    def make_ebom(self):
        self.ebom = list(csv.DictReader(self.rawtable))
        for row in self.ebom:
            for typ in row.keys():
                try:
                    row[typ] = self.converter.convert(typ, row[typ]) 
                except KeyError:
                    pass
        self.ebom_depth = max([row['Level'] for row in self.ebom])
        id_group = [0] * self.ebom_depth
        for row in self.ebom:
            id_group[row['Level'] - 1] = row['Name']
            try:
                row['Parent Name'] = id_group[row['Level'] - 2]
            except:
                row['Parent Name'] = 'NA'
        # print (self.ebom_depth)
    
    # def remove_item(self, name):
            # if row['']
    
    def filter_ebom(self, level):
        return [(row['Name'], row['Qty']) for row in self.ebom if row['Level'] == level]

    
    def return_ebom(self):
        return self.ebom if self.ebom_depth else None


class Comparer:
    def __init__(self, base, ref):
        self.base = base
        self.ref = ref
    
    def compare(self, typ):
        with open(os.path.join(folderpath, 'common.csv'), 'w', newline='') as cmnhandle:
            headline = ['Item Number', 'New Packer', 'Ref Packer', 'Short Description', 'Comments']

            cmnwriter = csv.DictWriter(cmnhandle, headline)
            cmnwriter.writeheader()

            (ebom_2_base_name, ebom_2_base_qty) = self.base.filter_ebom(2) 
            (ebom_2_ref_name, ebom_2_ref_qty) = self.base.filter_ebom(2)
                
            common_parts = [name for name in ebom_2_base_name if name in ebom_2_ref_name]
            base_unique_parts = [name for name in ebom_2_base_name if name not in ebom_2_ref_name]
            ref_unique_parts = [name for name in ebom_2_ref_name if name not in ebom_2_ref_name]

            comments = ['All matched', 'Qty changed from %d to %d', '' ]


    



table_1 = RawTable()
table_2 = RawTable()

folderpath = os.path.dirname(os.path.abspath(__file__))
filename_1 = 'base.csv'
fullpath_1 = os.path.join(folderpath, filename_1)
filename_2 = 'ref.csv'
fullpath_2 = os.path.join(folderpath, filename_2)

table_1.make_table(fullpath_1)
table_2.make_table(fullpath_2)

my_converter = ValConverter()
my_ebom = Ebom(table_1, my_converter)
my_ebom.make_ebom()

print (hasattr(my_converter, 'convert_qty'))
print (hasattr(my_converter.convert, '__call__'))