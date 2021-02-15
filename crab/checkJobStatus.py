#!/usr/bin/env python

from os import walk, path, chdir, system, popen

from collections import OrderedDict as od

effaccs = od()

for base, dirs, files in walk('Jobs'):
    if not base.count('sub_'): continue
    year = base.split('/')[1]
    sample = base.split('sub_')[1]
    subs = int(popen('ls -lrth %s | wc -l'%path.join(base,'runJobs*.sh')).read())
    done = int(popen('ls -lrth %s | wc -l'%path.join(base,'runJobs*.done')).read())
    print 'for sample %s %s: %g / %g jobs are done'%(year, sample, done, subs)
