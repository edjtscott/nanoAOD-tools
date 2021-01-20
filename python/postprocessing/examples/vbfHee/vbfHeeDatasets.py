#!/usr/bin/env python

from os import system

def run( cmd, dry=False ):
    print cmd
    if not dry: system(cmd)

signalsUL17 = ['/GluGluHToEE_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM', 
               '/VBFHToEE_M125_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM', 
               '/ttHJetToEE_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM'
              ]

backgroundsUL17 = ['/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM',
                   '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM',
                   '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM'#,
                   ## to be added later
                   #'/WWTo2L2Nu_TuneCP5_DoubleScattering_13TeV-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM'
                  ]

backgroundsRR = ['/EWK_LLJJ_MLL-50_MJJ-120_TuneCH3_PSweights_13TeV-madgraph-herwig7_corrected/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
                 '/EWK_LLJJ_MLL_105-160_SM_5f_LO_TuneCH3_13TeV-madgraph-herwig7_corrected/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
                 '/DYJetsToLL_M-105To160_TuneCP5_PSweights_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
                 '/DYJetsToLL_M-105To160_VBFFilter_TuneCP5_PSweights_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_VBFPostMGFilter_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM'
                ]

dataUL17 = ['/DoubleEG/Run2017B-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD', 
            '/DoubleEG/Run2017C-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD',
            '/DoubleEG/Run2017D-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD', 
            '/DoubleEG/Run2017E-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD', 
            '/DoubleEG/Run2017F-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD'
           ]

#print
#print
#for dset in signalsUL17:
#    print 'Dataset is %s:'%dset
#    run('dasgoclient -query="file dataset=%s"'%dset)
#    print
#print
#print
#for dset in backgroundsUL17:
#    print 'Dataset is %s:'%dset
#    run('dasgoclient -query="file dataset=%s"'%dset)
#    print
#print
#print
