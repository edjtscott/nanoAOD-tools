#!/usr/bin/env python

from os import walk, path, chdir, system, popen, listdir
from re import search
from collections import OrderedDict as od

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-f","--filt",type="str",default="",help="Add a requirement on the path name")
parser.add_option("-v","--verb",type="int",default=0,help="Verbosity")
(opts,args) = parser.parse_args()

effaccs = od()

for base, dirs, files in walk('Jobs'):
    if not base.count('sub_'): continue
    if not opts.filt=='' and not search(opts.filt,base): continue
    year = base.split('/')[1]
    sample = base.split('sub_')[1]
    subs = int(popen('ls -lrth %s | wc -l'%path.join(base,'runJobs*.sh')).read())
    done = int(popen('ls -lrth %s | wc -l'%path.join(base,'runJobs*.done')).read())
    if opts.verb > 0:
        subList = []
        doneList = []
        fileList = []
        for fName in files:
            if fName.endswith('.sh'): 
                subList.append( int(fName.split('_')[-1].split('.')[0]) )
                fileList.append( '%s_Skim.root'%popen('cat %s/%s | grep ".root"'%(base,fName)).read().split('.root')[0].split()[-1].split('/')[-1] )
            elif fName.endswith('.done'): doneList.append( int(fName.split('_')[-1].split('.')[0]) )
        for iFile,fNumber in enumerate(subList):
            if not fNumber in doneList:
                print 'Job number %g from path %s is not done'%(fNumber,base.replace('sub_',''))
                print 'Corresponding output file name is %s'%fileList[iFile]
    else: print 'for sample %s %s: %g / %g jobs are done'%(year, sample, done, subs)
