#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 14:13:33 2021

@author: gorangiudetti
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

feat = ["r2",	"r3",	"a3",	"r4",	"a4",	"d4",	"r5",	"a5",	"d5",	"r6",	"a6",	"d6",	"r7",	"a7",	"d7",	"r8",	"a8",	"d8",	"r9",	"a9",	"d9",	"r10",	"a10",	"d10",	"r11",	"a11",	"d11",	"r12",	"a12",	"d12",	"r13",	"a13",	"d13",	"r14",	"a14",	"d14",	"r15",	"a15",	"d15",	"r16",	"a16",	"d16",	"r17",	"a17",	"d17",	"r18",	"a18",	"d18",	"r19",	"a19",	"d19",	"r20",	"a20",	"d20",	"r21",	"a21",	"d21",	"r22",	"a22",	"d22",	"r23",	"a23",	"d23",	"r24",	"a24",	"d24",	"r25",	"a25",	"d25",	"r26",	"a26",	"d26",	"r27",	"a27",	"d27",	"r28",	"a28",	"d28",	"r29",	"a29",	"d29",	"r30",	"a30",	"d30",	"r31",	"a31",	"d31",	"r32",	"a32",	"d32",	"r33",	"a33",	"d33",	"r34",	"a34",	"d34",	"r35",	"a35",	"d35",	"r36",	"a36",	"d36",	"r37",	"a37",	"d37",	"r38",	"a38",	"d38",	"r39",	"a39",	"d39",	"r40",	"a40",	"d40",	"r41",	"a41",	"d41",	"r42",	"a42",	"d42",	"r43",	"a43",	"d43",	"r44",	"a44",	"d44",	"r45",	"a45",	"d45",	"r46",	"a46",	"d46",	"r47",	"a47",	"d47",	"r48",	"a48",	"d48",	"r49",	"a49",	"d49",]

NMI = []
for i in feat:
    o=open("./MI_not_rounded/MI_%s.txt" % i, "r")
    o1 = o.readlines()
    o2 = o1[3].strip().split()
    NMI.append(o2[6])
    o.close()
    
# print(feat)
# print(NMI)

zipped_lists = zip(NMI,feat)
sorted_pairs = sorted(zipped_lists, reverse=True)

tuples = zip(*sorted_pairs)
SNMI, Sfeat = [ list(tuple) for tuple in  tuples]

# print(SNMI)
# print(Sfeat)

df = pd.DataFrame(np.zeros((52052,len(SNMI))), columns=Sfeat)
print(df)

for x in Sfeat:
    f = open("all_%s_internal.txt" % x,"r")
    f1 = f.readlines()
    F = []
    for z in range(0,len(f1)):
        f2 = f1[z].strip().split()
        F.append(f2[1])
    df[x] = F
    df[x] = df[x].astype(float)
    f.close()


corrMatrix = df.corr()
print (corrMatrix)

# sns.heatmap(corrMatrix, annot = True)

# plt.show()

u, s, v = np.linalg.svd(corrMatrix, full_matrices=True)

print(u)
print(s)
print(v)

var_explained = np.round(s**2/np.sum(s**2), decimals=3)
var_explained
 
sns.barplot(x=list(range(1,len(var_explained)+1)),
            y=var_explained, color="limegreen")
plt.xlabel('SVs', fontsize=16)
plt.ylabel('Percent Variance Explained', fontsize=16)
plt.savefig('svd_scree_plot.png',dpi=100)

