#!/bin/usr/env python

from os import walk, path, chdir, system

from collections import OrderedDict as od

effaccs = od()

for base, dirs, files in walk('Jobs'):
    if not base.count('sub_'): continue
    if base.count('Data'): continue
    sample = base.split('sub_')[1]
    numerSum = 0.
    denomSum = 0.
    for iFile in range(min(5,len(files)//4)):
        with open(path.join(base,'runJobs_%g.log'%iFile)) as inFile:
            for line in inFile.readlines():
                if line.count('preselected entries from'): 
                    numerSum += float(line.split('Finally selected ')[1].split(' ')[0])
                    denomSum += float(line.split('root (')[1].split(' ')[0])
    effaccs[sample] = numerSum / denomSum

for key,val in effaccs.iteritems():
    print 'Sample %s has total eff*acc of %.7f'%(key,val)
