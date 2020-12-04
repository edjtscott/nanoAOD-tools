from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from numpy import cos, sqrt, exp, array
from math import pi


## to be added:
##   - year dependence
##   - data/MC dependence

class vbfHeeProducer(Module):
    def __init__(self, jetSelection, eleSelection, variables):
        self.jetSel = jetSelection
        self.eleSel = eleSelection
        self.variables = variables
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for floatName in self.variables.allFloatNames():
            self.out.branch(floatName, "F")
        for intName in self.variables.allIntNames():
            self.out.branch(intName, "I")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def fillElectron(self, ele, order):
        if ele is not None:
            self.out.fillBranch("%sElectronMass"%order, ele.mass)
            self.out.fillBranch("%sElectronPt"%order, ele.pt)
            self.out.fillBranch("%sElectronEta"%order, ele.eta)
            self.out.fillBranch("%sElectronPhi"%order, ele.phi)
            self.out.fillBranch("%sElectronIDMVA"%order, ele.mvaFall17V2Iso)
        else:
            for var in self.variables.electronVariables:
                self.out.fillBranch("%sElectron%s"%(order,var), -9999.)
            for var in self.variables.objectVariables:
                self.out.fillBranch("%sElectron%s"%(order,var), -9999.)

    def fillJet(self, jet, order):
        if jet is not None:
            self.out.fillBranch("%sJetMass"%order, jet.corr_JEC*jet.mass)
            self.out.fillBranch("%sJetPt"%order, jet.pt_nom)
            self.out.fillBranch("%sJetEta"%order, jet.eta)
            self.out.fillBranch("%sJetPhi"%order, jet.phi)
            self.out.fillBranch("%sJetID"%order, jet.jetId)
            self.out.fillBranch("%sJetPUJID"%order, jet.puId)
            self.out.fillBranch("%sJetQGL"%order, jet.qgl)
        else:
            for var in self.variables.jetVariables:
                self.out.fillBranch("%sJet%s"%(order,var), -9999.)
            for var in self.variables.objectVariables:
                self.out.fillBranch("%sJet%s"%(order,var), -9999.)

    def selectElectron(self, ele):
        if not ele.mvaFall17V2Iso_WP90: return False
        if not abs(ele.eta) < 2.5: return False
        if abs(ele.eta) > 1.44 and abs(ele.eta) > 1.57: return False
        return True

    def selectJet(self, jet):
        selected = True
        if not jet.jetId >= 5.5: return False
        if not jet.puId >= 3.5: return False
        if not abs(jet.eta) < 4.7: return False
        return True

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        ## electrons handling
        electrons = Collection(event, "Electron")
        leadEle = None
        subleadEle = None
        subsubleadEle = None
        for ele in filter(self.eleSel, electrons):
            if not self.selectElectron(ele): continue ## apply a fairly loose electron selection
            if leadEle is None:
                leadEle = ele
            elif subleadEle is None:
                subleadEle = ele
            elif subsubleadEle is None:
                subsubleadEle = ele
        self.fillElectron(leadEle, 'lead')
        self.fillElectron(subleadEle, 'sublead')
        self.fillElectron(subsubleadEle, 'subsublead')

        ## jet handling
        leadJet = None
        subleadJet = None
        subsubleadJet = None
        jets = Collection(event, "Jet")
        for jet in filter(self.jetSel, jets):
            if leadEle is not None:
                if jet.DeltaR(leadEle) < 0.4: continue
            if subleadEle is not None:
                if jet.DeltaR(subleadEle) < 0.4: continue
            if not self.selectJet(jet): continue ## apply a fairly loose jet selection
            if leadJet is None:
                leadJet = jet
            elif subleadJet is None:
                subleadJet = jet
            elif subsubleadJet is None:
                subsubleadJet = jet
        self.fillJet(leadJet, 'lead')
        self.fillJet(subleadJet, 'sublead')
        self.fillJet(subsubleadJet, 'subsublead')

        ## perform event selection
        eventSelected = False
        if leadEle is not None and subleadEle is not None: 
            if leadEle.pt > 35. and subleadEle.pt > 25.:
                eventSelected = True

        if eventSelected:
            ## dielectron system - FIXME modify this to a dedicated fill function
            dielectron = leadEle.p4() + subleadEle.p4()
            dielectronDPhi= abs(leadEle.phi - subleadEle.phi)
            while dielectronDPhi > pi:
                dielectronDPhi = abs(dielectronDPhi - 2 * pi)
            dielectronCosPhi= cos(dielectronDPhi)
            dielectronSigmaMoM = sqrt( (leadEle.pt/leadEle.energyErr)**2 + (subleadEle.pt/subleadEle.energyErr)**2 )
            self.out.fillBranch('dielectronMass', dielectron.M())
            self.out.fillBranch('dielectronPt', dielectron.Pt())
            self.out.fillBranch('dielectronEta', dielectron.Eta())
            self.out.fillBranch('dielectronPhi', dielectron.Phi())
            self.out.fillBranch('dielectronCosPhi', dielectronCosPhi)
            self.out.fillBranch('dielectronCosPhi', dielectronSigmaMoM)

            if leadJet is not None and subleadJet is not None:
                ## dijet system - FIXME modify this to a dedicated fill function
                dijet = leadEle.p4() + subleadEle.p4()
                dijetAbsDEta = abs(leadEle.eta - subleadEle.eta)
                dijetDPhi= abs(leadEle.phi - subleadEle.phi)
                while dijetDPhi > pi:
                    dijetDPhi = abs(dijetDPhi - 2 * pi)
                dijetAbsDPhiTrunc = dijetDPhi if abs(dijetDPhi) < 3.1 else 3.1
                dijetZep = abs( dielectron.Eta() - 0.5*(leadJet.eta+subleadJet.eta) )
                dijetCentrality = exp( -4. * ((dijetZep/dijetAllDEta)**2) )
                dijetMinDRJetEle = min( array( leadJet.DeltaR(leadEle),  leadJet.DeltaR(subleadEle), subleadJet.DeltaR(leadEle), subleadJet.DeltaR(subleadEle) ) )
                self.out.fillBranch('dijetMass', dijet.M())
                self.out.fillBranch('dijetPt', dijet.Pt())
                self.out.fillBranch('dijetEta', dijet.Eta())
                self.out.fillBranch('dijetPhi', dijet.Phi())
                self.out.fillBranch('dijetAbsDEta', dijetAbsDEta)
                self.out.fillBranch('dijetAbsDPhiTrunc', dijetAbsDPhiTrunc)
                self.out.fillBranch('dijetCentrality', dijetCentrality)
                self.out.fillBranch('dijetMinDRJetEle', dijetMinDRJetEle)

                ## higgs plus two jet system - FIXME modify this to a dedicated fill function
                higgssystem = dielectron + dijet
                self.out.fillBranch('higgssystemMass', higgssystem.M())
                self.out.fillBranch('higgssystemPt', higgssystem.Pt())
                self.out.fillBranch('higgssystemEta', higgssystem.Eta())
                self.out.fillBranch('higgssystemPhi', higgssystem.Phi())
            else:
                self.out.fillBranch('dijetMass', -9999.)
                self.out.fillBranch('dijetPt', -9999.)
                self.out.fillBranch('dijetEta', -9999.)
                self.out.fillBranch('dijetPhi', -9999.)
                self.out.fillBranch('dijetAbsDEta', -9999.)
                self.out.fillBranch('dijetAbsDPhiTrunc', -9999.)
                self.out.fillBranch('dijetCentrality', -9999.)
                self.out.fillBranch('dijetMinDRJetEle', -9999.)

                self.out.fillBranch('higgssystemMass', -9999.)
                self.out.fillBranch('higgssystemPt', -9999.)
                self.out.fillBranch('higgssystemEta', -9999.)
                self.out.fillBranch('higgssystemPhi', -9999.)
       
        return eventSelected


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
from PhysicsTools.NanoAODTools.postprocessing.examples.vbfHee.vbfHeeVariables import vbfHeeVars
vbfHeeModuleConstr = lambda: vbfHeeProducer(jetSelection=lambda j: j.pt > 20., eleSelection=lambda e: e.pt > 25., variables = vbfHeeVars)
