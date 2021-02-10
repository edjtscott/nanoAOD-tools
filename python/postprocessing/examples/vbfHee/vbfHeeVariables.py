## define the list of variables to be computed and stored for VBF Hee analysis

class VariableController():
    def __init__(self, orders):
        assert isinstance(orders,list)
        self.orders = orders
        self.objectVariables = ['En', 'Mass', 'Pt', 'Eta', 'Phi']
        self.electronVariables = ['IDMVA', 'SigmaE', 'Charge']
        self.jetVariables = ['QGL', 'ID', 'PUJID']
        self.eventVariables = ['leadJetDieleDPhi', 'leadJetDieleDEta', 'subleadJetDieleDPhi', 'subleadJetDieleDEta',
                               'dielectronMass', 'dielectronPt', 'dielectronEta', 'dielectronPhi', 'dielectronCosPhi', 'dielectronSigmaMoM', 'leadElectronPtOvM', 'subleadElectronPtOvM',
                               'dijetMass', 'dijetPt', 'dijetEta', 'dijetPhi', 'dijetAbsDEta', 'dijetDPhi', 'dijetMinDRJetEle', 'dijetCentrality', 'dijetDieleAbsDPhiTrunc', 'dijetDieleAbsDEta',
                               'higgssystemMass', 'higgssystemPt', 'higgssystemEta', 'higgssystemPhi'
                              ]
        self.jetPtSystematics = ['pt_jesTotalUp', 'pt_jesTotalDown', 'pt_jerUp', 'pt_jerDown']
        self.elePtSystematics = ['pt_ElPtScaleUp', 'pt_ElPtScaleDown']
        self.emptyVal = -999.

    def allFloatNames(self):
        ## to do: add in the full set of systematic variation names here
        floats = []
        for order in self.orders:
            for var in self.objectVariables:
               floats.append('%sJet%s'%(order,var))
               floats.append('%sElectron%s'%(order,var))
            for var in self.electronVariables:
               floats.append('%sElectron%s'%(order,var))
            for var in self.jetVariables:
               floats.append('%sJet%s'%(order,var))
            for var in ['En', 'Mass', 'Pt']:
               for systVar in self.jetPtSystematics:
                   floats.append('%sJet%s%s'%(order,var,self.getSystLabel(systVar)))
               for systVar in self.elePtSystematics:
                   floats.append('%sElectron%s%s'%(order,var,self.getSystLabel(systVar)))
        for var in self.eventVariables:
           floats.append('%s'%(var))
        for var in ['dijetMass', 'dijetPt', 'higgssystemMass', 'higgssystemPt']:
            for systVar in self.jetPtSystematics:
                varLabel = self.getSystLabel(systVar)
                floats.append('%s%s'%(var, varLabel))
        for var in ['leadElectronPtOvM', 'subleadElectronPtOvM', 'dielectronMass', 'dielectronPt', 'higgssystemMass', 'higgssystemPt']:
            for systVar in self.elePtSystematics:
                varLabel = self.getSystLabel(systVar)
                floats.append('%s%s'%(var, varLabel))
        return floats

    def allIntNames(self):
        ints = []
        return ints

    def getSystLabel(self, name):
        return '_%s'%name.split('_')[-1]


vbfHeeVars = VariableController(orders = ['lead', 'sublead', 'subsublead'])
