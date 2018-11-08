#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# [XNiu2 08-Nov-2018] 

import os
import re
import csv
import collections

# the point of making a new table is to add a column called "parent id" to extend it to a tree structure.
def make_table(origin):
    with open(origin, 'r', newline='') as header:
        head = header.readlines()
        # base = re.findall(r'\d{9}', head[0])
        # useful_items = []
        reader = csv.DictReader(head[2:])
        id_group = [0,0,0,0,0]
        reader_list = list(reader)
        for row in reader_list:
            id_group[int(row['Level'])-1] = row['Name']
            try:
                row['Parent Name'] = id_group[int(row['Level'])-2]
            except:
                row['Parent Name'] = 'NA'
            # print (row)

            # from below the codes are filtering the rows to write in file. 
            # Here it only allows the rows with usages and their level-3 child items
            # if row['Level'] == '2' and row['Usage']:
            #     writer.writerow(row)
            #     useful_items.append(row['Name'])
            # elif row['Level'] == '3' and row['Parent Name'] in useful_items:
            #     writer.writerow(row)
        return reader_list 

def compare(base, ref):
    with open(os.path.join(folderpath, 'common.csv'), 'w', newline='') as cmnhandle:
        head = ['Item Number', 'New Packer', 'Ref Packer', 'Short Description', 'Comments']

        cmnwriter = csv.DictWriter(cmnhandle, head)
        cmnwriter.writeheader()

        for row_1 in base:
            row_1['Comments'] = ''
            for row_2 in ref:
                if row_1['Level'] == '2' and row_2['Level'] == '2' and row_1['Name'] == row_2['Name']:
                    if row_1['Qty'] == row_2['Qty']:
                        row_1['Comments'] = 'Perfect Match'
                        cmnwriter.writerow(simp_row(row_1))
                        break
                    else:
                        row_1['Comments'] = 'Qty changed from %s to %s' % (row_2['Qty'], row_1['Qty'])
                        cmnwriter.writerow(simp_row(row_1))
                        break
            
            #Start to handle the drawing comparison
            # refreader = csv.DictReader(refhandle)
            if row_1['Comments'] == '':
                for row_2 in ref:
                    if row_2['Level'] == '3' and row_1['Level'] == '2' and get_drawing(row_1, base) == row_2['Name']:
                        row_1['Comments'] = 'share the same drawing %s' % (row_2['Name'])
                        cmnwriter.writerow(simp_row(row_1, row_2['Parent Name']))
                        break

            # Till here the corresponding part is still not found... 
            if row_1['Comments'] == '':
                if row_1['Level'] == '2':
                    row_1['Comments'] = 'Cannot find the corresponding part'
                    cmnwriter.writerow(simp_row(row_1))


def get_drawing(row, raw_tb):
    for gst_row in raw_tb:
        if gst_row['Level'] == '3' and gst_row['Type'] == 'ProE Drawing' and gst_row['Parent Name'] == row['Name']:
            return gst_row['Name']
         

def simp_row(long_row, refpn = ''):
    long_descr = long_row['Description']
    short_descr_list = []
    short_descr_list = re.findall(r'([\w ]*?,[ ]*[\w ]*?),[ ]*\d',long_descr)
    if not short_descr_list:
        short_descr_list = re.findall(r'([\w ]*?),[ ]*\d', long_descr)    
    if not short_descr_list:
        short_descr_list = re.findall(r'([\w ]*?),', long_descr)
    if not short_descr_list:
        short_descr = long_descr

    else:
        short_descr_list = short_descr_list[0].split(', ')
        short_descr_list.reverse()
        short_descr_list = list(map(lambda i: i.strip(),short_descr_list))
        try:
            short_descr = ' '.join(short_descr_list)
        except:
            short_descr = short_descr_list
        


    short_row = {}
    short_row['Item Number'] = long_row['Item Number']
    short_row['New Packer'] = long_row['Name']
    short_row['Short Description'] = short_descr

    if refpn == '':
        short_row['Ref Packer'] = long_row['Name']
    else:
        short_row['Ref Packer'] = refpn
    
    short_row['Comments'] = long_row['Comments']


    return short_row

folderpath = os.path.dirname(os.path.abspath(__file__))
filename_1 = '103130620.csv'
fullpath_1 = os.path.join(folderpath, filename_1)
filename_2 = '101706021.csv'
fullpath_2 = os.path.join(folderpath, filename_2)


compare(make_table(fullpath_1), make_table(fullpath_2))