#!/usr/bin/env python

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule import *
from  PhysicsTools.NanoAODTools.postprocessing.examples.vbfHee.vbfHeeModule import vbfHeeModuleConstrData, vbfHeeModuleConstrMC

from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *


#selection='''Sum$(Photon_pt > 18 && abs(Photon_eta)<2.5) > 1  
#             && (Sum$(Electron_pt > 10 && abs(Electron_eta<2.5)) || Sum$(Muon_pt > 10 && abs(Muon_eta<2.4)) || Sum$(Tau_pt > 15 && abs(Tau_eta<2.4)) > 1)
#             && Entry$ < 10'''

#selection='''Sum$(Electron_pt > 25 && abs(Electron_eta<2.5)) > 1
#             && Entry$ < 100'''

selection='''Sum$(Electron_pt > 25 && abs(Electron_eta<2.5)) > 1'''

#files=["/hadoop/cms/store/user/hmei/nanoaod_runII/HHggtautau/HHggtautau_Era2018_private_v2_20201005/test_nanoaod_1.root"]
#files=["root://cms-xrd-global.cern.ch//store/mc/RunIISummer19UL17NanoAOD/GluGluHToEE_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_mc2017_realistic_v6-v1/00000/D1F68AEE-C601-1B43-8C4E-C2BEA41A5A45.root"]
files=["root://cms-xrd-global.cern.ch//store/data/Run2017B/DoubleEG/NANOAOD/UL2017_02Dec2019-v1/280000/9517812B-75C7-BF48-88E7-F5E4FB39210D.root"]
#files=!FILES!

PrefireCorr2016 = lambda : PrefCorr("L1prefiring_jetpt_2016BtoH.root", "L1prefiring_jetpt_2016BtoH", "L1prefiring_photonpt_2016BtoH.root", "L1prefiring_photonpt_2016BtoH")
PrefireCorr2017 = lambda : PrefCorr('L1prefiring_jetpt_2017BtoF.root', 'L1prefiring_jetpt_2017BtoF', 'L1prefiring_photonpt_2017BtoF.root', 'L1prefiring_photonpt_2017BtoF')

#p=PostProcessor(!OUTDIR!,files,       
p=PostProcessor(".",files,       
                  selection.replace('\n',''),
                  branchsel="keep_and_drop_inputs.txt",
                  outputbranchsel="keep_and_drop_outputs.txt",
                  #modules=[puAutoWeight_2018(),jetmetUncertainties2018(),muonScaleRes2018(),vbfHeeModuleConstrMC()],
                  #modules=[puAutoWeight_2017(),jetmetUncertainties2017(),PrefireCorr2017(),muonScaleRes2017(),vbfHeeModuleConstrMC()],
                  modules=[jetmetUncertainties2017(),vbfHeeModuleConstrData()],
                  provenance=True)

print p.branchsel._ops
print p.outputbranchsel._ops
p.run()

print "DONE"
