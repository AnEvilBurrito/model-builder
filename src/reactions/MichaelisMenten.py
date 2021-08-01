from .Reactions import Reactions

class MichaelisMenten(Reactions):

    def __init__(self, forwardSpecie: str, backwardSpecie: str, Vmax_f: float = 10, Km_b: float = 100, Vmax_b: float = 10, Km_f: float = 100):

        super().__init__(forwardSpecie, backwardSpecie)
    
        self.type = "MichaelisMenten"
        self.params = {
            'vmaxf': Vmax_f,
            'kmf': Km_f,
            'vmaxb': Vmax_b,
            'kmb': Km_b
        }

        self.__renameParams()

    def __renameParams(self):
        
        vmaxf = 'vm_{fs}_to_{bs}'.format(fs=self.fs[0], bs=self.bs[0])
        kmf = 'km_{fs}_to_{bs}'.format(fs=self.fs[0], bs=self.bs[0])
        vmaxb = 'vm_{bs}_to_{fs}'.format(fs=self.fs[0], bs=self.bs[0])
        kmb = 'km_{bs}_to_{fs}'.format(fs=self.fs[0], bs=self.bs[0])

        self.paramNames['vmaxf'] = vmaxf
        self.paramNames['kmf'] = kmf
        self.paramNames['vmaxb'] = vmaxb
        self.paramNames['kmb'] = kmb

    def computeForward(self, stateVars: dict):

        fs = stateVars[self.fs[0]]
        

        return (self.params['vmaxf'] * fs) / (self.params['kmf'] + fs)

    def computeBackward(self, stateVars: dict):

        bs = stateVars[self.bs[0]]

        return (self.params['vmaxb'] * bs) / (self.params['kmb'] + bs)

    def getEqHeaderStr(self, index):
        return "{forward} <=> {backward} :R{i}".format(forward=self.fs[0], backward=self.bs[0], i=index)

    def getForwardEqStr(self):
        
        return "{vmaxf} * {fs} / ({kmf} + {fs})".format(vmaxf=self.paramNames['vmaxf'], kmf=self.paramNames['kmf'], fs=self.fs[0])

    def getBackwardEqStr(self):
        
        return "{vmaxb} * {bs} / ({kmb} + {bs})".format(vmaxb=self.paramNames['vmaxb'], kmb=self.paramNames['kmb'], bs=self.bs[0])
