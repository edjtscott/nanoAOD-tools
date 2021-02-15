#!/usr/bin/env python

from os import walk, path, chdir, system

from collections import OrderedDict as od

effaccs = od()
effaccs['2016'] = od()
effaccs['2017'] = od()
effaccs['2018'] = od()

for base, dirs, files in walk('Jobs'):
    if not base.count('sub_'): continue
    if base.count('Data'): continue
    year = base.split('/')[1]
    sample = base.split('sub_')[1]
    numerSum = 0.
    denomSum = 0.
    completeList = []
    for fName in files:
        if fName.count('.done'): completeList.append( fName.split('.done')[0].split('_')[1] )
    for iFile in completeList:
        with open(path.join(base,'runJobs_%g.log'%int(iFile))) as inFile:
            for line in inFile.readlines():
                if line.count('preselected entries from'): 
                    numerSum += float(line.split('Finally selected ')[1].split(' ')[0])
                    denomSum += float(line.split('root (')[1].split(' ')[0])
    effaccs[year][sample] = numerSum / denomSum if denomSum > 0. else -999.

for year in effaccs.keys():
    print 'Considering %s'%year
    for key,val in effaccs[year].iteritems():
        print 'Sample %s has total eff*acc of %.7f'%(key,val)

print effaccs
