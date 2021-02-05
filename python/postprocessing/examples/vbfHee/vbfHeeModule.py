from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from numpy import cos, sqrt, exp, array
from math import pi


## to be added:
##  - full set of central object weights (ele SFs, others?)

class vbfHeeProducer(Module):
    def __init__(self, isData, year, jetSelection, eleSelection, variables):
        print 'ED DEBUG initialising module'
        self.isData = isData
        self.year = str(year)
        self.jetSel = jetSelection
        self.eleSel = eleSelection
        self.variables = variables
        print 'ED DEBUG done initialising module'

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print 'ED DEBUG in beginFile'
        self.out = wrappedOutputTree
        for floatName in self.variables.allFloatNames():
            self.out.branch(floatName, "F")
        for intName in self.variables.allIntNames():
            self.out.branch(intName, "I")
        self.out.branch("centralObjectWeight", "F")
        self.out.branch("weight", "F")
        for var in self.jetSystmatics:
            varLabel = '_%s'%var.split('_')[-1]
            self.out.branch('dijetMass%s'%varLabel)
            self.out.branch('dijetPt%s'%varLabel)
            self.out.branch('higgssystemMass%s'%variationLabel)
            self.out.branch('higgssystemPt%s'%variationLabel)
        print 'ED DEBUG leaving beginFile'

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def fillElectron(self, ele, order, ptVariation=None, variationName=''):
        if ele is not None:
            if self.isData or ptVariation is None: actualPt = ele.pt
            elif ptVariation is not None: actualPt = ptVariation
            theP4 = ele.p4(corr_pt=actualPt)
            self.out.fillBranch("%sElectronEn%s"%order, theP4.E(), variationName)
            self.out.fillBranch("%sElectronMass%s"%order, theP4.M(), variationName)
            self.out.fillBranch("%sElectronPt%s"%order, theP4.Pt(), variationName)
            if ptVariation is None:
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

    def fillJet(self, jet, order, ptVariation=None, variationName=''):
        if jet is not None:
            if self.isData: actualPt = jet.pt
            elif ptVariation is not None: actualPt = ptVariation
            else: actualPt = jet.pt_nom
            self.out.fillBranch("%sJetEn%s"%order, jet.p4(corr_pt=actualPt).E(), variationName)
            self.out.fillBranch("%sJetMass%s"%order, jet.p4(corr_pt=actualPt).M(), variationName)
            self.out.fillBranch("%sJetPt%s"%order, actualPt, variationName)
            if ptVariation is None:
                self.out.fillBranch("%sJetEta"%order, jet.eta)
                self.out.fillBranch("%sJetPhi"%order, jet.phi)
                self.out.fillBranch("%sJetID"%order, jet.jetId)
                self.out.fillBranch("%sJetPUJID"%order, jet.puId)
                self.out.fillBranch("%sJetQGL"%order, jet.qgl)
        else:
            for var in self.variables.jetVariables:
                self.out.fillBranch("%sJet%s"%(order,var), self.variables.emptyVal)
            for var in self.variables.objectVariables:
                self.out.fillBranch("%sJet%s"%(order,var), self.variables.emptyVal)

    def fillDielectron(self, leadEle, subleadEle, leadPtVariation=None, subleadPtVariation=None, variationName=''):
        if self.isData or variationName=='': 
            actualLeadPt = leadEle.pt
            actualSubleadPt = subleadEle.pt
        elif variationName!='': 
            actualLeadPt = leadPtVariation
            actualSubleadPt = subleadPtVariation
        dielectron = leadEle.p4(corr_pt=actualLeadPt) + subleadEle.p4(corr_pt=actualSubleadPt)
        dielectronDPhi = deltaPhi(leadEle.phi,subleadEle.phi)
        dielectronCosPhi= cos(dielectronDPhi)
        dielectronSigmaMoM = sqrt( (leadEle.energyErr/leadEle.p4(corr_pt=actualLeadPt).E())**2 + (subleadEle.energyErr/subleadEle.p4(corr_pt=actualSubleadPt).E())**2 )
        self.out.fillBranch('leadElectronPtOvM%s', leadEle.pt/dielectron.M(), variationName)
        self.out.fillBranch('subleadElectronPtOvM%s', subleadEle.pt/dielectron.M(), variationName)
        self.out.fillBranch('dielectronMass%s', dielectron.M(), variationName)
        self.out.fillBranch('dielectronPt%s', dielectron.Pt(), variationName)
        if variationName=='':
            self.out.fillBranch('dielectronEta', dielectron.Eta())
            self.out.fillBranch('dielectronPhi', dielectron.Phi())
            self.out.fillBranch('dielectronCosPhi', dielectronCosPhi)
            self.out.fillBranch('dielectronSigmaMoM', dielectronSigmaMoM)

    def fillDijet(self, leadEle, subleadEle, leadJet, subleadJet, leadElePtVariation=None, subleadElePtVariation=None, leadJetPtVariation=None, subleadJetPtVariation=None, variationName=''):
        if self.isData or variationName=='': 
            actualLeadElePt = leadEle.pt
            actualSubleadElePt = subleadEle.pt
        elif variationName!='': 
            actualLeadElePt = leadElePtVariation
            actualSubleadElePt = subleadElePtVariation
        dielectron = leadEle.p4(corr_pt=actualLeadElePt) + subleadEle.p4(corr_pt=actualSubleadElePt)
        if leadJet is not None:
            self.out.fillBranch('leadJetDieleDPhi', deltaPhi(leadJet.eta, dielectron.Phi()))
            self.out.fillBranch('leadJetDieleDEta', leadJet.eta - dielectron.Eta())
        else:
            self.out.fillBranch('leadJetDieleDPhi', self.variables.emptyVal)
            self.out.fillBranch('leadJetDieleDEta', self.variables.emptyVal)
        if subleadJet is not None:
            self.out.fillBranch('subleadJetDieleDPhi', deltaPhi(subleadJet.phi, dielectron.Phi()))
            self.out.fillBranch('subleadJetDieleDEta', subleadJet.eta - dielectron.Eta())
        else:
            self.out.fillBranch('subleadJetDieleDPhi', self.variables.emptyVal)
            self.out.fillBranch('subleadJetDieleDEta', self.variables.emptyVal)
        if leadJet is not None and subleadJet is not None:
            if self.isData: 
                actualLeadJetPt = leadJet.pt
                actualSubleadJetPt = subleadJet.pt
            elif ptVariation is not None: 
                actualLeadJetPt = leadJetPtVariation
                actualSubleadJetPt = subleadJetPtVariation
            else: 
                actualLeadJetPt = leadJet.pt_nom
                actualSubleadJetPt = subleadJet.pt_nom
            dijet = leadJet.p4(corr_pt=actualLeadJetPt) + subleadJet.p4(corr_pt=actualSubleadJetPt)
            dijetAbsDEta = abs(leadJet.eta - subleadJet.eta)
            dijetDPhi = deltaPhi(leadJet.phi, subleadJet.phi)
            dijetZep = abs( dielectron.Eta() - 0.5*(leadJet.eta+subleadJet.eta) )
            dijetCentrality = exp( -4. * ((dijetZep/dijetAbsDEta)**2) ) if abs(dijetAbsDEta)>1e-6 else self.variables.emptyVal
            dijetMinDRJetEle = min( array( [leadJet.DeltaR(leadEle),  leadJet.DeltaR(subleadEle), subleadJet.DeltaR(leadEle), subleadJet.DeltaR(subleadEle)] ) )
            dijetDieleAbsDPhi = abs( deltaPhi(dijet.Phi(), dielectron.Phi()) )
            dijetDieleAbsDPhiTrunc = dijetDieleAbsDPhi if abs(dijetDieleAbsDPhi) < 3.1 else 3.1
            dijetDieleAbsDEta = abs(dijet.Eta() - dielectron.Eta())
            self.out.fillBranch('dijetMass%s', dijet.M(), variationName)
            self.out.fillBranch('dijetPt%s', dijet.Pt(), variationName)
            if variationName=='':
                self.out.fillBranch('dijetEta', dijet.Eta())
                self.out.fillBranch('dijetPhi', dijet.Phi())
                self.out.fillBranch('dijetAbsDEta', dijetAbsDEta)
                self.out.fillBranch('dijetDPhi', dijetDPhi)
                self.out.fillBranch('dijetCentrality', dijetCentrality)
                self.out.fillBranch('dijetMinDRJetEle', dijetMinDRJetEle)
                self.out.fillBranch('dijetDieleAbsDPhiTrunc', dijetDieleAbsDPhiTrunc)
                self.out.fillBranch('dijetDieleAbsDEta', dijetDieleAbsDEta)

            higgssystem = dielectron + dijet
            self.out.fillBranch('higgssystemMass%s', higgssystem.M(), variationName)
            self.out.fillBranch('higgssystemPt%s', higgssystem.Pt(), variationName)
            if variationName=='':
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
            self.out.fillBranch('dijetDieleAbsDEta', self.variables.emptyVal)

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
        if not self.isData: 
            if not jet.pt_nom > 25.: return False
        else:
            if not jet.pt > 25.: return False
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

    def setWeightMC(self, genWeight, weights, weightTol=1000.):
        centralObjectWeight = 1.
        for weight in weights:
            centralObjectWeight *= weight
        if centralObjectWeight < 1./weightTol or centralObjectWeight > weightTol:
            raise RuntimeError('Unphysical central weight of %.5f found'%centralObjectWeight)
        self.out.fillBranch('centralObjectWeight', centralObjectWeight)
        self.out.fillBranch('weight', centralObjectWeight*genWeight)

    def setWeightData(self):
        self.out.fillBranch('centralObjectWeight', 1.)
        self.out.fillBranch('weight', 1.)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        print 'ED DEBUG beginning analyse function'
        ## first apply trigger - now to both MC and data
        if not event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL: return False

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

            ## to do: loop over these variations when filling the jet
            self.fillJet(leadJet, 'lead')
            self.fillJet(subleadJet, 'sublead')
            self.fillJet(subsubleadJet, 'subsublead')
            for var in self.jetPtSystematics:
                varLabel = '_%s'%var.split('_')[-1]
                self.fillJet(leadJet, 'lead', getattr(leadJet,var), varLabel)
                self.fillJet(subleadJet, 'sublead', getattr(leadJet,var), varLabel)
                self.fillJet(subsubleadJet, 'subsublead', getattr(leadJet,var), varLabel)

            self.fillDielectron(leadEle, subleadEle) ## dielectron system
            self.fillDijet(leadEle, subleadEle, leadJet, subleadJet) ## dijet and dijet plus diphoton system

            ## now set the event weight using the relevant factors
            if not self.isData:
                evtWeights = []
                if self.year.count('2016') or self.year.count('2017'):
                    evtWeights.append(event.L1PreFiringWeight_Nom)
                self.setWeightMC(event.genWeight, evtWeights)
            else: 
                self.setWeightData()

            print 'ED DEBUG exiting analyse function'
            return True

        else: 
            print 'ED DEBUG exiting analyse function'
            return False


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
from PhysicsTools.NanoAODTools.postprocessing.examples.vbfHee.vbfHeeVariables import vbfHeeVars
jetThresh = 20.
eleThresh = 25.
vbfHeeModuleConstrData2016 = lambda: vbfHeeProducer(isData=True,  year=2016, jetSelection=lambda j: j.pt > jetThresh, eleSelection=lambda e: e.pt > eleThresh, variables = vbfHeeVars)
vbfHeeModuleConstrMC2016   = lambda: vbfHeeProducer(isData=False, year=2016, jetSelection=lambda j: j.pt > jetThresh, eleSelection=lambda e: e.pt > eleThresh, variables = vbfHeeVars)
vbfHeeModuleConstrData2017 = lambda: vbfHeeProducer(isData=True,  year=2017, jetSelection=lambda j: j.pt > jetThresh, eleSelection=lambda e: e.pt > eleThresh, variables = vbfHeeVars)
vbfHeeModuleConstrMC2017   = lambda: vbfHeeProducer(isData=False, year=2017, jetSelection=lambda j: j.pt > jetThresh, eleSelection=lambda e: e.pt > eleThresh, variables = vbfHeeVars)
vbfHeeModuleConstrData2018 = lambda: vbfHeeProducer(isData=True,  year=2018, jetSelection=lambda j: j.pt > jetThresh, eleSelection=lambda e: e.pt > eleThresh, variables = vbfHeeVars)
vbfHeeModuleConstrMC2018   = lambda: vbfHeeProducer(isData=False, year=2018, jetSelection=lambda j: j.pt > jetThresh, eleSelection=lambda e: e.pt > eleThresh, variables = vbfHeeVars)
