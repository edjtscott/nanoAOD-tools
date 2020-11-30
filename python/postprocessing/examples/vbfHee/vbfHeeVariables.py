## define the list of variables to be computed and stored for VBF Hee analysis

class VariableController():
    def __init__(self, orders):
        assert isinstance(orders,list)
        self.orders = orders
        self.objectVariables = ['Mass','Pt','Eta','Phi']
        self.electronVariables = ['IDMVA']
        self.jetVariables = ['QGL','ID','PUJID']

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
        return floats

    def allIntNames(self):
        ints = []
        return ints


vbfHeeVars = VariableController(orders = ['lead','sublead','subsublead'])
