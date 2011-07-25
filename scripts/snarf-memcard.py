#!/usr/bin/env python

## grabs all images off digital rebel T1i and puts them in
## ~/photos-canon

import os
import subprocess
import re
import tempfile


mount_target = None
for line in subprocess.Popen('dmesg | tail', stdout=subprocess.PIPE, shell=True).communicate()[0].split('\n'):
    m = re.match(".* sd[a-z]: (sd[a-z][0-9]) .*", line)
    if m:
        mount_target = m.group(1)
if mount_target:
    mount = tempfile.mkdtemp()
    print "trying to mount",mount_target,mount
    subprocess.call('mount /dev/%s %s' % (mount_target, mount))
else:
    mount = '/mnt/foo'

base = os.path.join(mount,'DCIM/100CANON')
print "Sucking photos from",base,mount_target

files = os.listdir(base)
if len(files) == 0:
    print "Found nothing"
    sys.exit(-1)

files = filter(lambda x: 'THM' not in x, files)


for f in files:
    subprocess.call('cp %s %s' % (os.path.join(base,f), '/home/mike/photos-canon'), shell=True)
    subprocess.call('chown mike %s' % (os.path.join('/home/mike/photos-canon', f)), shell=True)
    subprocess.call('chgrp mike %s' % (os.path.join('/home/mike/photos-canon', f)), shell=True)
    print f
        
print "rotating all downloaded photos"
for f in files:
    if f[-3:] != 'JPG':
        continue
    
    f = os.path.join('/home/mike/photos-canon/',f)
    subprocess.call(['exiftran', '-i', '-a', f])

subprocess.call(['python', '/home/mike/projects/photo/scripts/thumbnailer.py'])
