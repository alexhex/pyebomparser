#!usr/bin/python3
#-*-coding:utf-8-*
# [XNiu2 2018-11-05] 

import os
import re
import csv


def simp_row(long_row):
    header = ['Item Number', 'New ']
    with open(long_row, 'r', newline='') as header:
        head = header.readlines()
        base = re.findall(r'\d{9}', head[0])
        with open(str(base[0])+'.csv', 'w', newline='') as ebomfile:
            reader = csv.DictReader(head[3:])
            head = reader.fieldnames
            head[-1] = 'Short Description'
            # print (head)
            writer = csv.DictWriter(ebomfile, head) 
            writer.writeheader()
            for row in reader:
                if row['Level'] == '2':
                    long_descr = row['Description']
                    short_descr = ''
                    short_descr_list = []
                    print (long_descr)
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
            return short_descr


simp_row('origin.csv')