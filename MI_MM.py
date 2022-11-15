#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 18:06:09 2021

@author: madhubani
"""

import math
import sys


lab = sys.argv[1]

o = open("all_HOMO.txt","r")
p = open("all_%s_internal.txt" % lab,"r")

# o = open("parity.rtf","r")
# p = open("dice.rtf" ,"r")

o1 = o.readlines()
p1 = p.readlines()
g = []
X = []
Y = []


for z in range(0,len(o1)):
    k = []
    o2 = o1[z].strip().split()
    p2 = p1[z].strip().split()
    k.append(round(float(o2[0]),2))
    k.append(round(float(p2[1]),1))
    X.append(round(float(o2[0]),2))
    Y.append(round(float(p2[1]),1))
    g.append(k)


g1 = []
X1 = []
Y1 = []
for z in range(0,len(o1)):
    k = []
    o2 = o1[z].strip().split()
    p2 = p1[z].strip().split()
    k.append(round(float(o2[0]),2))
    k.append(round(float(p2[1]),1))
    g1.append(k)
    X1.append(round(float(o2[0]),2))
    Y1.append(round(float(p2[1]),1))  

# for z in range(0,len(o1)):
#     k = []
#     o2 = o1[z].strip().split()
#     p2 = p1[z].strip().split()
#     k.append(o2[0])
#     k.append(p2[1])
#     X.append(o2[0])
#     Y.append(p2[1])
#     g.append(k)


# g1 = []
# X1 = []
# Y1 = []
# for z in range(0,len(o1)):
#     k = []
#     o2 = o1[z].strip().split()
#     p2 = p1[z].strip().split()
#     k.append(o2[0])
#     k.append(p2[1])
#     g1.append(k)
#     X1.append(o2[0])
#     Y1.append(p2[1])  


for z in range(0,len(g)):
    g1[z] = tuple(g1[z])
    
X1 = list(set(tuple(X1)))
Y1 = list(set(tuple(Y1)))    
g1 = list(set(g1))

f = []
fh = []
fi = []
for i in g1:
    zz = g.count(list(i))
    s = []
    s.append(i)
    s.append(zz/len(g))
    f.append(tuple(s))
    #print(str(list(i))+ " appears "+ str(zz) +" times")

for i in X1:
    zz = X.count(i)
    s = []
    s.append(i)
    s.append(zz/len(X))
    fh.append(tuple(s))
    print(str(i)+ " appears "+ str(zz) +" times")
    
for i in Y1:
    zz = Y.count(i)
    s = []
    s.append(i)
    s.append(zz/len(Y))
    fi.append(tuple(s))
    #print(str(i)+ " appears "+ str(zz) +" times")    
    
 
d = dict(f)
dh = dict(fh)
di = dict(fi)


MI = 0
H1 = 0
H2 = 0

for x in X1:
    for y in Y1:
        t = []
        t.append(x)
        t.append(y)
        t = tuple(t)
        if t in d:
            MI += d[t]*math.log(d[t]/(dh[x]*di[y]),2)

for x in X1:          
    H1 += -dh[x]*math.log(dh[x],2)
    
for y in Y1:          
    H2 += -di[y]*math.log(di[y],2)

NMI = 2*MI/(H1+H2)    
    
output=open("MI_%s.txt" % lab,"w")
output.write("The MI value for %s is: " % lab + str(MI)+"\n")
output.write("The Entropy of HOMO energies is: " + str(H1)+"\n")
output.write("The Entropy for %s is: " % lab + str(H2)+"\n")
output.write("The Normalized MI for %s is: " % lab + str(NMI)+"\n")
output.close        
print("The MI value for %s is: " % lab + str(MI))   