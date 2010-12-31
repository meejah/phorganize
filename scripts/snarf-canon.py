#!/usr/bin/env python

## grabs all images off digital rebel T1i and puts them in
## ~/photos-canon

import os
import subprocess

print "downloading photos"

os.chdir('/home/mike/photos-canon')
subprocess.call(['gphoto2','--force-overwrite', '--get-all-files'])

print "rotating all downloaded photos"
## find names of all the files
sub = subprocess.Popen(['gphoto2','-L'], stdout=subprocess.PIPE)

files = []
for line in sub.communicate()[0].split('\n'):
    line = line.strip()
    if len(line) == 0 or line[0] != '#':
        continue
    vals = line.split()
    files.append(vals[1].strip())

for f in files:
    if f[-3:] != 'JPG':
        continue
    
    f = os.path.join('/home/mike/photos-canon/',f)
    subprocess.call(['exiftran', '-i', '-a', f])

subprocess.call(['python', '/home/mike/projects/photo/scripts/thumbnailer.py'])

## to delete everything

##subprocess.call(['gphoto2','--delete-all-files', '--recurse'])
