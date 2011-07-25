#!/usr/bin/env python

import sys
import os
import tempfile
import shutil
import pyexiv2
sys.path.insert(0,'/home/mike/python')

from flickrapi import FlickrAPI
from flickr import MikeFlickr

flickrAPIKey = open('/home/mike/flickr.key', 'r').read()
flickrSecret = open('/home/mike/flickr.secret', 'r').read()

fapi = None
fapi = FlickrAPI(flickrAPIKey, flickrSecret)

if len(sys.argv) < 2:
    print "usage: %s JPEG [JPEG]" % sys.argv[0]
    sys.exit(-1)

token = fapi.getToken(browser="lynx")##,perms="delete")
mikeapi = MikeFlickr(fapi,flickrAPIKey,token)

## methods

def userinput(prompt):
    rtn = ''
    while len(rtn) == 0:
        rtn = raw_input(prompt).strip()
    return rtn

##
## now, upload everything on the command line (unless we have already
## backed it up)
##

toupload = []
for jpeg in sys.argv[1:]:
    if os.stat(jpeg).st_size == 0:
        print "zero-size:",jpeg,"...skipping"
        continue

    if os.path.split(jpeg)[-1].split('.')[-1].lower() in ['avi','mov']:
        print "movie, skipping:",jpeg
        continue        

    toupload.append(jpeg)

print "found",len(toupload),"images to upload."

tmpdir = tempfile.mkdtemp()

uploadinfo = []

for jpeg in toupload:
    print jpeg
    os.system('feh --full-screen --draw-filename "%s"' % jpeg)
    while True:
        name = userinput("Name:")
        desc = userinput("Description:")
        tags = userinput("Tags:")

        if name.strip() == '.' and desc.strip() == '.' and tags.strip() == '.':
            print "skipping"
            print
            break

        print name
        print
        print desc
        print "tags:",tags
        good = False
        while not good:
            yn = userinput("ok ?")
            yn = yn.strip().lower()
            if len(yn) > 0 and (yn[0] is 'y' or yn[0] is 'n'):
                good = True
        if yn[0] == 'y':
            uploadinfo.append( (jpeg, name, desc, tags) )
            break


for (jpeg, name, desc, tags) in uploadinfo:
    print "Uploading:",jpeg

    try:
        tmpjpeg = os.path.join(tmpdir,os.path.split(jpeg)[-1])
        shutil.copyfile(jpeg, tmpjpeg)
        md = pyexiv2.ImageMetadata(tmpjpeg)
        md.read()

        md['Exif.Image.Copyright'] = 'mike warren'
        print '   removing:',
        for k in ['Exif.Photo.DateTimeDigitized',
                  'Exif.Photo.DateTimeOriginal',
                  'Exif.Image.Make',
                  'Exif.Image.Model',
                  'Exif.Image.DateTime'
                  ]:
            print k,
            try:
                del md[k]
            except:
                print "(not present)",
            print ",",

        print
        print name
        print description
        print tags
        
        md.write()
        photoid = mikeapi.upload(tmpjpeg,
                                 title=name,
                                 description=desc,
                                 tags=tags,
                                 isPublic=True,
                                 isFriend=False,
                                 isFamily=False)
        os.unlink(tmpjpeg)
        print "done; id=",photoid
    except:
        print "ERROR"

shutil.rmtree(tmpdir)
