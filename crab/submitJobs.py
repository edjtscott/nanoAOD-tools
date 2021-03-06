#!/usr/bin/env python

from os import system, path, getcwd

def submitJob( subdir, theCmd, jobNumber, dryRun=False ):
  subName = '%s/runJobs_%g.sh'%(subdir,jobNumber)
  with open('submitTemplate.sh') as inFile:
    with open(subName,'w') as outFile:
      for line in inFile.readlines():
        if '!CMD!' in line:
          line = line.replace('!CMD!','"%s"'%theCmd)
        elif '!MYDIR!' in line:
          line = line.replace('!MYDIR!',getcwd())
        elif '!NAME!' in line:
          line = line.replace('!NAME!',subName.replace('.sh',''))
        outFile.write(line)
  subCmd = 'qsub -q hep.q -o %s -e %s -l h_vmem=12G -l h_rt=10:0:0 %s' %(subName.replace('.sh','.log'), subName.replace('.sh','.err'), subName) 
  print
  print subCmd
  if not dryRun:
    system(subCmd)


from Utilities.General.cmssw_das_client import get_data as das_query

def safe_das_query( search, cmd ):
    output = das_query( search, cmd=cmd )
    if not 'data' in output:
        raise Exception('Your das query has not worked properly - check your proxy is valid')
    return output


def processDataType(year, dsets, isSig, isBkg, isData, dry=False, filePrepend='root://cms-xrd-global.cern.ch/', baseOutDir='.'):
    if sum( [int(isSig), int(isBkg), int(isData)] ) > 1: raise Exception('Can only be one of signal, background, or data!')
    procType = None
    if isSig: procType = 'Signal'
    elif isBkg: procType = 'Background'
    elif isData: procType = 'Data'
    for dset in dsets:
        if isData: dsetName = '%s_%s'%(dset.split('/')[1],dset.split('/')[2])
        else: dsetName = dset.split('/')[1]
        print 'Processing the dataset %s'%dsetName
        subDir = '%s/Jobs/%g/%s/sub_%s'%(getcwd(), year, procType, dsetName)
        if not path.isdir(subDir): system('mkdir -p %s'%subDir)
        outDir = '%s/%s/%s'%(baseOutDir, procType, dsetName)
        if not path.isdir(outDir): system('mkdir -p %s'%outDir)
        fileData = safe_das_query('file dataset=%s'%dset, cmd='dasgoclient')['data']
        for iFile, fInfo in enumerate(fileData):
            fName = filePrepend+fInfo['file'][0]['name']
            cmd = './run_postproc_vbfHee.py --files %s --outDir %s -y %g '%(fName, outDir, year)
            if isData: 
              cmd += '--isData '
              cmd += '--runPeriod %s '%filter( lambda run : dset.count(run), ['Run2016B', 'Run2016C', 'Run2016D', 'Run2016E', 'Run2016F', 'Run2016G', 'Run2016H', 'Run2017B', 'Run2017C', 'Run2017D', 'Run2017E', 'Run2017F', 'Run2018A', 'Run2018B', 'Run2018C','Run2018D'] )[0][-1]
            submitJob( subDir, cmd, iFile, dryRun=dry )


from optparse import OptionParser
parser = OptionParser()
parser.add_option("-d","--dryRun",action="store_true", default=False)
parser.add_option("-y","--year",type="int", default=2017)
parser.add_option("--runData",action="store_true", default=False)
parser.add_option("--runSig",action="store_true", default=False)
parser.add_option("--runBkg",action="store_true", default=False)
(opts,args) = parser.parse_args()

baseOutDir = '%s/Outputs/Pass8/%g'%(getcwd(), opts.year)

from  PhysicsTools.NanoAODTools.postprocessing.examples.vbfHee.vbfHeeDatasets import signals, backgrounds, datas

if opts.runSig:  processDataType(opts.year, dsets=signals[opts.year], isSig=True, isBkg=False, isData=False, dry = opts.dryRun, baseOutDir = baseOutDir)

if opts.runBkg:  processDataType(opts.year, dsets=backgrounds[opts.year], isSig=False, isBkg=True, isData=False, dry = opts.dryRun, baseOutDir = baseOutDir)

if opts.runData: processDataType(opts.year, dsets=datas[opts.year], isSig=False, isBkg=False, isData=True, dry = opts.dryRun, baseOutDir = baseOutDir)
