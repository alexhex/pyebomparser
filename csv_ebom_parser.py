#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# [XNiu2 08-Nov-2018] 

import os
import re
import csv
import collections

def make_table(origin):
    with open(origin[0], 'r', newline='') as header, open(origin[1], 'w', newline='') as ebomfile:
        head = header.readlines()
        # base = re.findall(r'\d{9}', head[0])
        useful_items = []
        reader = csv.DictReader(head[2:])
        id_group = [0,0,0,0,0]
        head = reader.fieldnames
        head[-1] = 'Parent Name'
        # print (head)
        writer = csv.DictWriter(ebomfile, head) 
        writer.writeheader()
        for row in reader:
            id_group[int(row['Level'])-1] = row['Name']
            try:
                row['Parent Name'] = id_group[int(row['Level'])-2]
            except:
                row['Parent Name'] = 'NA'
            # print (row)

            # from below the codes are filtering the rows to write in file. 
            # Here it only allows the rows with usages and their level-3 child items
            if row['Level'] == '2' and row['Usage']:
                writer.writerow(row)
                useful_items.append(row['Name'])
            elif row['Level'] == '3' and row['Parent Name'] in useful_items:
                writer.writerow(row)
        

def compare(base, ref):
    with open(base, 'r', newline='') as basehandle, open(ref, 'r', newline='') as refhandle, open('common.csv', 'w', newline='') as cmnhandle:
        basereader = csv.DictReader(basehandle)
        refreader = csv.DictReader(refhandle)
        head = ['Item Number', 'New Packer', 'Ref Packer', 'Short Description', 'Comments']

        cmnwriter = csv.DictWriter(cmnhandle, head)
        cmnwriter.writeheader()

        reflist = list(refreader)
        

        for row_1 in basereader:
        #     print ('row_1')
        #     print (row_1['Name'])
        #     refreader = csv.DictReader(refhandle)
            row_1['Comments'] = ''
            for item in reflist:
                if row_1['Level'] == '2' and item['Level'] == '2' and row_1['Name'] == item['Name']:
                    if row_1['Qty'] == item['Qty']:
                        row_1['Comments'] = 'All right then~'
                        cmnwriter.writerow(simp_row(row_1))
                        break
                    else:
                        row_1['Comments'] = 'Qty changed from %s to %s' % (item['Qty'], row_1['Qty'])
                        cmnwriter.writerow(simp_row(row_1))
                        break
            
        #     #Start to handle the drawing comparison
            # refreader = csv.DictReader(refhandle)
            if row_1['Comments'] == '':
                for item in reflist:
                    if item['Level'] == '3' and row_1['Level'] == '2' and get_drawing(row_1, 'base.csv') == item['Name']:
                        row_1['Comments'] = 'Drawing the same with Part Number %s' % item['Parent Name']
                        cmnwriter.writerow(simp_row(row_1, item['Parent Name']))
                        break

def get_drawing(row, raw_tb):
    with open(raw_tb, 'r', newline='') as handle:
        reader = csv.DictReader(handle)
        for gst_row in reader:
            if gst_row['Level'] == '3' and gst_row['Type'] == 'ProE Drawing' and gst_row['Parent Name'] == row['Name']:
                return gst_row['Name']
         

        # with open('report.md', 'w') as resulthandle:
        #     resulthandle.writelines('# Comparison Result\n')
        #     resulthandle.writelines('## Common Components\n')
        #     resulthandle.writelines('|Item Number|New Packer|DUT|Short Description|Comment|\n')
        #     resulthandle.writelines('|           |          |   |                 |       |\n')

        #     basereader = csv.DictReader(basehandle)
        #     refreader = csv.DictReader(refhandle)
        #     for row in basereader:
        #         for row_2 in refreader:
        #             if row['Level'] == 2 and row_2['Level'] == 2 and row['Name'] == row_2['Name']:
        #                 if row['Qty'] == row_2['Qty']:
        #                     resulthandle.


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
    if refpn == '':
        short_row['Ref Packer'] = long_row['Name']
    else:
        short_row['Ref Packer'] = refpn
    short_row['Short Description'] = short_descr
    short_row['Comments'] = long_row['Comments']

    return short_row

make_table(['103130620.csv','base.csv'])
make_table(['101706021.csv', 'ref.csv'])
compare('base.csv', 'ref.csv')