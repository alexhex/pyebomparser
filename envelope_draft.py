#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# [XNiu2 03-Nov-2018] 

import os
import re
import matplotlib.pyplot as plt


folderpath = os.path.dirname(os.path.abspath(__file__))
filename = "in.txt"
filepath = os.path.join(folderpath, filename)
points = []

with open(filepath, 'r') as reading:
    lines = reading.readlines()
    for line in lines:
        team = re.split(' =', line)
        team = re.split(',', team[-1])
        # print (team)
        if len(team) >= 2:
            new_team = list(map(float,team))
            # print (new_team)
            new_team.append(new_team[0]) # to close the envelope, add the first point to the last
            points.append(new_team)

    # print (points)

labels = ['isolated', 'plugged below', 'unplugged']

# generate a list like, 0, 2, 4, 6
for i in list(range(len(points)))[0::2]:
    # print (i)
    # 
    plt.plot(points[i+1], points[i], label = labels.pop(0) )

plt.xlabel('(ABOVE)        DIFFERENTIAL PRESSURE (PSI)       (BELOW)')
plt.ylabel('(COMPRESSION)        LOAD(LBF)       (TENSION)')
plt.legend()
plt.show()

