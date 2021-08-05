from .Reactions import Reactions
# from Reactions import Reactions

class MassAction(Reactions):

    # Simplified Mass Action with only two forward specie and one backward specie,
    # with molecularities of 1

    def __init__(self, forwardSpecie1: str, forwardSpecie2: str, backwardSpecie: str = '_Auto', name='', Ka: float = 0.001, Kd: float = 0.01):

        if backwardSpecie == '_Auto':
            backwardSpecie = forwardSpecie1 + 'u' + forwardSpecie2
        super().__init__([forwardSpecie1, forwardSpecie2], backwardSpecie, name)
        self.type = "MassAction"

        self.params = {
            'ka': Ka,
            'kd': Kd
        }

        self.__renameParams()


    def __renameParams(self):

        kaStr = "ka_{f1}_{f2}".format(f1=self.fs[0], f2=self.fs[1])
        kdStr = "kd_{b1}".format(b1=self.bs[0])

        self.paramNames['ka'] = kaStr
        self.paramNames['kd'] = kdStr

    def computeForward(self, stateVars: dict):

        fs1 = stateVars[self.fs[0]]
        fs2 = stateVars[self.fs[1]]

        return self.params['ka'] * fs1 * fs2

    def computeBackward(self, stateVars: dict):

        b1 = stateVars[self.bs[0]]

        return self.params['kd'] * b1

    def getEqHeaderStr(self, index):
        return "{forward1} + {forward2} <=> {backward} :R{i}".format(forward1=self.fs[0], forward2=self.fs[1], backward=self.bs[0], i=index)

    def getForwardEqStr(self):
        
        return "{ka} * {fs1} * {fs2}".format(ka=self.paramNames['ka'], fs1=self.fs[0], fs2=self.fs[1])

    def getBackwardEqStr(self):
        
        return "{kd} * {bs}".format(kd=self.paramNames['kd'], bs=self.bs[0])


if __name__ == "__main__":
    
    ma = MassAction('Sos', 'Grb2')
    print(ma.fs, ma.bs)
    print(ma.params)
    print(ma.paramNames)
