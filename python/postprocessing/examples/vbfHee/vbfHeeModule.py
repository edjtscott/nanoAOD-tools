from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from numpy import cos, sqrt, exp, array
from math import pi


## to be added:
##  - year dependence
##  - function to add event weight (product of gen weight, pre-firing, SFs, anything else)

class vbfHeeProducer(Module):
    def __init__(self, isData, jetSelection, eleSelection, variables):
        self.isData = isData
        self.jetSel = jetSelection
        self.eleSel = eleSelection
        self.variables = variables

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
            self.out.fillBranch("%sElectronEn"%order, ele.p4().E())
            self.out.fillBranch("%sElectronMass"%order, ele.mass)
            self.out.fillBranch("%sElectronPt"%order, ele.pt)
            self.out.fillBranch("%sElectronEta"%order, ele.eta)
            self.out.fillBranch("%sElectronPhi"%order, ele.phi)
            self.out.fillBranch("%sElectronIDMVA"%order, ele.mvaFall17V2Iso)
            self.out.fillBranch("%sElectronSigmaE"%order, ele.energyErr)
            self.out.fillBranch("%sElectronCharge"%order, ele.charge)
        else:
            for var in self.variables.electronVariables:
                self.out.fillBranch("%sElectron%s"%(order,var), self.variables.emptyVal)
            for var in self.variables.objectVariables:
                self.out.fillBranch("%sElectron%s"%(order,var), self.variables.emptyVal)

    def fillJet(self, jet, order):
        if jet is not None:
            self.out.fillBranch("%sJetEn"%order, jet.p4(corr_pt=jet.pt_nom).E())
            self.out.fillBranch("%sJetMass"%order, jet.p4(corr_pt=jet.pt_nom).M())
            self.out.fillBranch("%sJetPt"%order, jet.pt_nom)
            self.out.fillBranch("%sJetEta"%order, jet.eta)
            self.out.fillBranch("%sJetPhi"%order, jet.phi)
            self.out.fillBranch("%sJetID"%order, jet.jetId)
            self.out.fillBranch("%sJetPUJID"%order, jet.puId)
            self.out.fillBranch("%sJetQGL"%order, jet.qgl)
            if not self.isData:
                self.out.fillBranch("%sJetPtJerUp"%order, jet.pt_jerUp)
                self.out.fillBranch("%sJetPtJerDown"%order, jet.pt_jerDown)
                self.out.fillBranch("%sJetPtJecUp"%order, jet.pt_jesTotalUp)
                self.out.fillBranch("%sJetPtJecDown"%order, jet.pt_jesTotalDown)
            else:
                self.out.fillBranch("%sJetPtJerUp"%order, self.variables.emptyVal)
                self.out.fillBranch("%sJetPtJerDown"%order, self.variables.emptyVal)
                self.out.fillBranch("%sJetPtJecUp"%order, self.variables.emptyVal)
                self.out.fillBranch("%sJetPtJecDown"%order, self.variables.emptyVal)
        else:
            for var in self.variables.jetVariables:
                self.out.fillBranch("%sJet%s"%(order,var), self.variables.emptyVal)
            for var in self.variables.objectVariables:
                self.out.fillBranch("%sJet%s"%(order,var), self.variables.emptyVal)

    def fillDielectron(self, leadEle, subleadEle):
        dielectron = leadEle.p4() + subleadEle.p4()
        dielectronDPhi = deltaPhi(leadEle.phi,subleadEle.phi)
        dielectronCosPhi= cos(dielectronDPhi)
        dielectronSigmaMoM = sqrt( (leadEle.energyErr/leadEle.p4().E())**2 + (subleadEle.energyErr/subleadEle.p4().E())**2 )
        self.out.fillBranch('leadElectronPtOvM', leadEle.pt/dielectron.M())
        self.out.fillBranch('subleadElectronPtOvM', subleadEle.pt/dielectron.M())
        self.out.fillBranch('dielectronMass', dielectron.M())
        self.out.fillBranch('dielectronPt', dielectron.Pt())
        self.out.fillBranch('dielectronEta', dielectron.Eta())
        self.out.fillBranch('dielectronPhi', dielectron.Phi())
        self.out.fillBranch('dielectronCosPhi', dielectronCosPhi)
        self.out.fillBranch('dielectronSigmaMoM', dielectronSigmaMoM)

    def fillDijet(self, leadEle, subleadEle, leadJet, subleadJet):
        if leadJet is not None and subleadJet is not None:
            dielectron = leadEle.p4() + subleadEle.p4()
            dijet = leadJet.p4() + subleadJet.p4()
            dijetAbsDEta = abs(leadJet.eta - subleadJet.eta)
            dijetDPhi = deltaPhi(leadJet.phi, subleadJet.phi)
            dijetZep = abs( dielectron.Eta() - 0.5*(leadJet.eta+subleadJet.eta) )
            dijetCentrality = exp( -4. * ((dijetZep/dijetAbsDEta)**2) ) if abs(dijetAbsDEta)>1e-6 else self.variables.emptyVal
            dijetMinDRJetEle = min( array( [leadJet.DeltaR(leadEle),  leadJet.DeltaR(subleadEle), subleadJet.DeltaR(leadEle), subleadJet.DeltaR(subleadEle)] ) )
            dijetDieleAbsDPhi = abs( deltaPhi(dijet.Phi(), dielectron.Phi()) )
            dijetDieleAbsDPhiTrunc = dijetDieleAbsDPhi if abs(dijetDieleAbsDPhi) < 3.1 else 3.1
            self.out.fillBranch('dijetMass', dijet.M())
            self.out.fillBranch('dijetPt', dijet.Pt())
            self.out.fillBranch('dijetEta', dijet.Eta())
            self.out.fillBranch('dijetPhi', dijet.Phi())
            self.out.fillBranch('dijetAbsDEta', dijetAbsDEta)
            self.out.fillBranch('dijetDPhi', dijetDPhi)
            self.out.fillBranch('dijetCentrality', dijetCentrality)
            self.out.fillBranch('dijetMinDRJetEle', dijetMinDRJetEle)
            self.out.fillBranch('dijetDieleAbsDPhiTrunc', dijetDieleAbsDPhiTrunc)

            higgssystem = dielectron + dijet
            self.out.fillBranch('higgssystemMass', higgssystem.M())
            self.out.fillBranch('higgssystemPt', higgssystem.Pt())
            self.out.fillBranch('higgssystemEta', higgssystem.Eta())
            self.out.fillBranch('higgssystemPhi', higgssystem.Phi())
        else:
            self.out.fillBranch('dijetMass', self.variables.emptyVal)
            self.out.fillBranch('dijetPt', self.variables.emptyVal)
            self.out.fillBranch('dijetEta', self.variables.emptyVal)
            self.out.fillBranch('dijetPhi', self.variables.emptyVal)
            self.out.fillBranch('dijetAbsDEta', self.variables.emptyVal)
            self.out.fillBranch('dijetDPhi', self.variables.emptyVal)
            self.out.fillBranch('dijetCentrality', self.variables.emptyVal)
            self.out.fillBranch('dijetMinDRJetEle', self.variables.emptyVal)
            self.out.fillBranch('dijetDieleAbsDPhiTrunc', self.variables.emptyVal)

            self.out.fillBranch('higgssystemMass', self.variables.emptyVal)
            self.out.fillBranch('higgssystemPt', self.variables.emptyVal)
            self.out.fillBranch('higgssystemEta', self.variables.emptyVal)
            self.out.fillBranch('higgssystemPhi', self.variables.emptyVal)

    def selectElectron(self, ele):
        if not ele.mvaFall17V2Iso_WP90: return False
        if not abs(ele.eta) < 2.5: return False
        if abs(ele.eta) > 1.44 and abs(ele.eta) < 1.57: return False
        return True

    def selectJet(self, jet):
        if not jet.jetId >= 5.5: return False
        if jet.pt < 50. and not jet.puId >= 3.5: return False 
        if not abs(jet.eta) < 4.7: return False
        return True

    def selectEvent(self, leadEle, subleadEle):
        if leadEle is None or subleadEle is None: return False
        if not leadEle.pt > 35.: return False
        if not subleadEle.pt > 25.: return False
        theMass = (leadEle.p4() + subleadEle.p4()).M()
        if not leadEle.pt > theMass/3.: return False
        if not subleadEle.pt > theMass/4.: return False
        if not (theMass>80. and theMass<180.): return False
        return True

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        ## first apply trigger - now to both MC and data
        if not (event.HLT_Ele32_WPTight_Gsf_L1DoubleEG or event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL): return False

        ## electron handling
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

        ## perform event selection and fill variables
        if self.selectEvent(leadEle, subleadEle):
            self.fillElectron(leadEle, 'lead')
            self.fillElectron(subleadEle, 'sublead')
            self.fillElectron(subsubleadEle, 'subsublead')

            self.fillJet(leadJet, 'lead')
            self.fillJet(subleadJet, 'sublead')
            self.fillJet(subsubleadJet, 'subsublead')

            self.fillDielectron(leadEle, subleadEle) ## dielectron system
            self.fillDijet(leadEle, subleadEle, leadJet, subleadJet) ## dijet and dijet plus diphoton system

            return True

        else: return False


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
from PhysicsTools.NanoAODTools.postprocessing.examples.vbfHee.vbfHeeVariables import vbfHeeVars
vbfHeeModuleConstrData = lambda: vbfHeeProducer(isData=True, jetSelection=lambda j: j.pt > 20., eleSelection=lambda e: e.pt > 25., variables = vbfHeeVars)
vbfHeeModuleConstrMC = lambda: vbfHeeProducer(isData=False, jetSelection=lambda j: j.pt > 20., eleSelection=lambda e: e.pt > 25., variables = vbfHeeVars)
