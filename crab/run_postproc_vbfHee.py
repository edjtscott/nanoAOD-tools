#!/usr/bin/env python

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-r","--runPeriod",default="")
parser.add_option("-y","--year",default="2017")
parser.add_option("-o","--outDir",default=".")
parser.add_option("-f","--files",default=None)
parser.add_option("-d","--isData",action="store_true", default=False)
parser.add_option("-l","--local",action="store_true", default=False)
(opts,args) = parser.parse_args()
opts.runPeriod = str(opts.runPeriod)
opts.year = str(opts.year)
opts.outDir = str(opts.outDir)

if opts.files is None:
    opts.files=["root://cms-xrd-global.cern.ch//store/mc/RunIISummer19UL17NanoAOD/GluGluHToEE_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_mc2017_realistic_v6-v1/00000/D1F68AEE-C601-1B43-8C4E-C2BEA41A5A45.root"]
    #opts.files=["root://cms-xrd-global.cern.ch//store/data/Run2017B/DoubleEG/NANOAOD/UL2017_02Dec2019-v1/280000/9517812B-75C7-BF48-88E7-F5E4FB39210D.root"]
else:
     opts.files = str(opts.files).split(',')

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from  PhysicsTools.NanoAODTools.postprocessing.examples.vbfHee.vbfHeeModule import vbfHeeModuleConstrData, vbfHeeModuleConstrMC

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import jetmetUncertainties2016, jetmetUncertainties2017, jetmetUncertainties2018, jetmetUncertainties2018Data
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import createJMECorrector
jetmetUncertainties2017DataB = createJMECorrector(isMC=False, dataYear=2017, runPeriod="B")
jetmetUncertainties2017DataC = createJMECorrector(isMC=False, dataYear=2017, runPeriod="C")
jetmetUncertainties2017DataD = createJMECorrector(isMC=False, dataYear=2017, runPeriod="D")
jetmetUncertainties2017DataE = createJMECorrector(isMC=False, dataYear=2017, runPeriod="E")
jetmetUncertainties2017DataF = createJMECorrector(isMC=False, dataYear=2017, runPeriod="F")

from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import PrefCorr
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puAutoWeight_2016, puAutoWeight_2017, puAutoWeight_2018
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import muonScaleRes2016, muonScaleRes2017, muonScaleRes2018

if opts.local:
    selection='''Sum$(Electron_pt > 25 && abs(Electron_eta<2.5)) > 1
                 && Entry$ < 100'''
else:
    selection='''Sum$(Electron_pt > 25 && abs(Electron_eta<2.5)) > 1'''

PrefireCorr2016 = lambda : PrefCorr("L1prefiring_jetpt_2016BtoH.root", "L1prefiring_jetpt_2016BtoH", "L1prefiring_photonpt_2016BtoH.root", "L1prefiring_photonpt_2016BtoH")
PrefireCorr2017 = lambda : PrefCorr('L1prefiring_jetpt_2017BtoF.root', 'L1prefiring_jetpt_2017BtoF', 'L1prefiring_photonpt_2017BtoF.root', 'L1prefiring_photonpt_2017BtoF')

theModules = []
if opts.isData: 
    if opts.year.count('2017'):
        if opts.runPeriod.count('B'):
            theModules += [jetmetUncertainties2017DataB]
        elif opts.runPeriod.count('C'):
            theModules += [jetmetUncertainties2017DataC]
        elif opts.runPeriod.count('D'):
            theModules += [jetmetUncertainties2017DataD]
        elif opts.runPeriod.count('E'):
            theModules += [jetmetUncertainties2017DataE]
        elif opts.runPeriod.count('F'):
            theModules += [jetmetUncertainties2017DataF]
        theModules += [vbfHeeModuleConstrData]
    elif opts.year.count('2018'):
        theModules += [jetmetUncertainties2018Data, vbfHeeModuleConstrData]
else:
    if opts.year.count('2016'):
        theModules += [puAutoWeight_2016, jetmetUncertainties2016, PrefireCorr2016, muonScaleRes2016, vbfHeeModuleConstrMC]
    elif opts.year.count('2017'):
        theModules += [puAutoWeight_2017, jetmetUncertainties2017, PrefireCorr2017, muonScaleRes2017, vbfHeeModuleConstrMC]
    elif opts.year.count('2018'):
        theModules += [puAutoWeight_2018, jetmetUncertainties2018, muonScaleRes2018, vbfHeeModuleConstrMC]

p=PostProcessor( opts.outDir,
                 opts.files,       
                 selection.replace('\n',''),
                 branchsel="keep_and_drop_inputs.txt",
                 outputbranchsel="keep_and_drop_outputs.txt",
                 modules=[apply(mod) for mod in theModules],
                 provenance=True )

print p.branchsel._ops
print p.outputbranchsel._ops
p.run()

print "DONE"
