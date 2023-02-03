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
from sklearn.preprocessing import StandardScaler
#feat = ["r2",	"r3",	"a3",	"r4",	"a4",	"d4",	"r5",	"a5",	"d5",	"r6",	"a6",	"d6",	"r7",	"a7",	"d7",	"r8",	"a8",	"d8",	"r9",	"a9",	"d9",	"r10",	"a10",	"d10",	"r11",	"a11",	"d11",	"r12",	"a12",	"d12",	"r13",	"a13",	"d13",	"r14",	"a14",	"d14",	"r15",	"a15",	"d15",	"r16",	"a16",	"d16",	"r17",	"a17",	"d17",	"r18",	"a18",	"d18",	"r19",	"a19",	"d19",	"r20",	"a20",	"d20",	"r21",	"a21",	"d21",	"r22",	"a22",	"d22",	"r23",	"a23",	"d23",	"r24",	"a24",	"d24",	"r25",	"a25",	"d25",	"r26",	"a26",	"d26",	"r27",	"a27",	"d27",	"r28",	"a28",	"d28",	"r29",	"a29",	"d29",	"r30",	"a30",	"d30",	"r31",	"a31",	"d31",	"r32",	"a32",	"d32",	"r33",	"a33",	"d33",	"r34",	"a34",	"d34",	"r35",	"a35",	"d35",	"r36",	"a36",	"d36",	"r37",	"a37",	"d37",	"r38",	"a38",	"d38",	"r39",	"a39",	"d39",	"r40",	"a40",	"d40",	"r41",	"a41",	"d41",	"r42",	"a42",	"d42",	"r43",	"a43",	"d43",	"r44",	"a44",	"d44",	"r45",	"a45",	"d45",	"r46",	"a46",	"d46",	"r47",	"a47",	"d47",	"r48",	"a48",	"d48",	"r49",	"a49",	"d49"]
#feat = ["d13", "d31", "r12", "r30", "r31", "r11", "r13", "a31", "a13", "r29", "r10", "r14", "r20", "a30", "a12", "a20", "a14", "a29", "a11", "d30", "d12", "d14"]
feat = ["d13", "d31", "r12", "r30", "r31", "r11", "r13", "a31", "a13", "r29", "r10", "r14", "r20", "a30", "a12", "a20", "a14", "a29", "a11"]

#for i in feat1:
#    if i not in feat:
#        feat.append(i)

NMI = []
for i in feat:
    o=open("MI_%s.txt" % i, "r")
    #o = open("NAMD/MI_NAMD_%s.txt" % i, "r")
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

df = pd.DataFrame(np.zeros((1092,len(SNMI))), columns=Sfeat)
#print(df)

for x in Sfeat:
    f = open("all_%s_internal_clean1.txt" % x,"r")
    f1 = f.readlines()
    F = []
    for z in range(0,len(f1)):
        f2 = f1[z].strip().split()
        F.append(f2[1])
    df[x] = F
    df[x] = df[x].astype(float)
    f.close()
#print(df)
x = df.loc[:, Sfeat].values
print(x)
x = StandardScaler().fit_transform(x)
x = pd.DataFrame(x, columns=Sfeat)
print(x)
corrMatrix = df.corr()
#print(corrMatrix)

#sns.heatmap(corrMatrix, annot = True)

df_small = df.iloc[:,:]

correlation_mat = df_small.corr()


sns.heatmap(correlation_mat, annot = True)
plt.savefig('Correlation_Matrix.png',dpi=600)


plt.show()

E, V = np.linalg.eig(correlation_mat)


print("Eigenvalues are here \n")
print(E[:2])
print("V vectors are here \n")
print(V[:2])

var_explained = np.round(E**2/np.sum(E**2), decimals=3)
PR = (np.sum(var_explained))**2/np.sum(var_explained**2)
print(PR)
#var_explained

sns.barplot(x=list(range(1,len(var_explained)+1)),
            y=var_explained, color="limegreen")
plt.xlabel('SVs', fontsize=16)
plt.ylabel('Percent Variance Explained', fontsize=16)
plt.savefig('svd_scree_plot_scaled.png',dpi=600)

w = open("coeff_output.txt","w")
w.write("Eigenvalues:\t{:.3f}\t\t\t{:.3f}\n".format(E[0],E[1]))

for j in range(len(V)):
    for i in range(2):
        w.write("\t\t{:.3f} ".format((V[i][j])**2)+feat[j])
    w.write("\n")
#
#for i in range(2):
#    w.write("Eigenvalue = {:.3f}, Coefficients of eigenvector are:\n".format(E[i]))
#    for j in range(len(V)):
#        w.write("{:.3f}".format((V[i][j])**2)+feat[j]+" ")
#    w.write("\n")
w.close()
