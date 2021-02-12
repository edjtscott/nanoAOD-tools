#!/usr/bin/env python

from os import system

def run( cmd, dry=False ):
    print cmd
    if not dry: system(cmd)

signals = {}
backgrounds = {}
datas= {}

signals[2017] = ['/GluGluHToEE_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM', 
                 '/VBFHToEE_M125_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM', 
                 '/ttHJetToEE_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM', 
                 '/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8_storeWeights/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM', 
                 '/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8_storeWeights/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM'
                ]

backgrounds[2017] = ['/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM',
                     '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM',
                     '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM'
                    ]

#backgrounds[2017] += ['/EWK_LLJJ_MLL-50_MJJ-120_TuneCH3_PSweights_13TeV-madgraph-herwig7_corrected/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
#                      '/EWK_LLJJ_MLL_105-160_SM_5f_LO_TuneCH3_13TeV-madgraph-herwig7_corrected/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
#                      '/DYJetsToLL_M-105To160_TuneCP5_PSweights_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
#                      '/DYJetsToLL_M-105To160_VBFFilter_TuneCP5_PSweights_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_VBFPostMGFilter_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM'
#                     ]

datas[2017] = ['/DoubleEG/Run2017B-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD', 
               '/DoubleEG/Run2017C-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD',
               '/DoubleEG/Run2017D-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD', 
               '/DoubleEG/Run2017E-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD', 
               '/DoubleEG/Run2017F-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD'
              ]


backgrounds[2016] = ['/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer19UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM',
                     '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM', 
                     '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM'
                    ]

datas[2016] = ['/DoubleEG/Run2016B-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD',
               '/DoubleEG/Run2016C-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD',
               '/DoubleEG/Run2016D-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD',
               '/DoubleEG/Run2016E-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD',
               '/DoubleEG/Run2016F-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD',
               '/DoubleEG/Run2016G-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD',
               '/DoubleEG/Run2016H-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD'
              ]


backgrounds[2018] = ['/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM',
                     '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM',
                     '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM'
                    ]

datas[2018] = ['/EGamma/Run2018A-UL2018_MiniAODv1_NanoAODv2-v1/NANOAOD',
               '/EGamma/Run2018B-UL2018_MiniAODv1_NanoAODv2-v1/NANOAOD', ## FIXME why is Run C missing for UL 18?
               '/EGamma/Run2018D-UL2018_MiniAODv1_NanoAODv2-v1/NANOAOD'
              ]
