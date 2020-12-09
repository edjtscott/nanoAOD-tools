## define the list of variables to be computed and stored for VBF Hee analysis

class VariableController():
    def __init__(self, orders):
        assert isinstance(orders,list)
        self.orders = orders
        self.objectVariables = ['Mass', 'Pt', 'Eta', 'Phi']
        self.electronVariables = ['IDMVA', 'SigmaE']
        self.jetVariables = ['QGL', 'ID', 'PUJID', 'PtJerUp', 'PtJerDown', 'PtJecUp', 'PtJecDown']
        self.eventVariables = ['dielectronMass', 'dielectronPt', 'dielectronEta', 'dielectronPhi', 'dielectronCosPhi', 'dielectronSigmaMoM', 
                               'dijetMass', 'dijetPt', 'dijetEta', 'dijetPhi', 'dijetAbsDEta', 'dijetAbsDPhiTrunc', 'dijetMinDRJetEle', 'dijetCentrality', 'dijetDieleDPhi', 
                               'higgssystemMass', 'higgssystemPt', 'higgssystemEta', 'higgssystemPhi'
                              ]

    def allFloatNames(self):
        floats = []
        for order in self.orders:
            for var in self.objectVariables:
               floats.append('%sJet%s'%(order,var))
               floats.append('%sElectron%s'%(order,var))
            for var in self.electronVariables:
               floats.append('%sElectron%s'%(order,var))
            for var in self.jetVariables:
               floats.append('%sJet%s'%(order,var))
        for var in self.eventVariables:
           floats.append('%s'%(var))
        return floats

    def allIntNames(self):
        ints = []
        return ints


vbfHeeVars = VariableController(orders = ['lead', 'sublead', 'subsublead'])
