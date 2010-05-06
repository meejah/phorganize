

import os

for f in os.listdir('.'):
    if f.lower() != f:
        cmd = 'mv %s %s' % (f, f.lower())
        print cmd
        os.system(cmd)
