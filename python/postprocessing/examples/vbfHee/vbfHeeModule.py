from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


## to be added:
##   - event variables
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
            print 'ED DEBUG adding branch with name %s'%floatName
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

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        ## electrons handling
        electrons = Collection(event, "Electron")
        leadEle = None
        subleadEle = None
        subsubleadEle = None
        for ele in filter(self.eleSel, electrons):
            ##apply extra selections here
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
            ##apply extra selections here
            if jet.DeltaR(leadEle) < 0.4 or jet.DeltaR(subleadEle) < 0.4: continue
            if leadJet is None:
                leadJet = jet
            elif subleadJet is None:
                subleadJet = jet
            elif subsubleadJet is None:
                subsubleadJet = jet
        self.fillJet(leadJet, 'lead')
        self.fillJet(subleadJet, 'sublead')
        self.fillJet(subsubleadJet, 'subsublead')

        ## add some per-event variables, like dielectron mass, here
       
        ## perform event selection
        eventSelected = False
        if leadEle is not None and subleadEle is not None: eventSelected = True
        return eventSelected


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
from PhysicsTools.NanoAODTools.postprocessing.examples.vbfHee.vbfHeeVariables import vbfHeeVars
vbfHeeModuleConstr = lambda: vbfHeeProducer(jetSelection=lambda j: j.pt > 20., eleSelection=lambda e: e.pt > 25., variables = vbfHeeVars)
