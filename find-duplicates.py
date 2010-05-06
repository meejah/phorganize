#!/usr/bin/env python

import sys
import os
import subprocess
from sha import sha


PHOTOS = '/home/mike/photos'


sums = {}

def process(root):
    for x in os.listdir(root):
        path = os.path.join(root,x)

        if os.path.isdir(path):
            process(path)
            continue

        sum = sha(open(path,'r').read()).hexdigest()
        print " ",sum,path
        
        if sums.has_key(sum):
            sums[sum].append(path)
        else:
            sums[sum] = [path]

process(PHOTOS)
print "done. Looking for duplicates"

for x in sums.keys():
    if len(sums[x]) > 1:
        print "DUPEs:",x,':',sums[x]
