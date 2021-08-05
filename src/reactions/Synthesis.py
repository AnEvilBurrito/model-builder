from .Reactions import Reactions

class Synthesis(Reactions):

    def __init__(self, backwardSpecies, KSyn: float = 0.01):
        super().__init__("None", backwardSpecies)
        self.type = 'Syn'
        self.params = {
            'ksyn': KSyn
        }
        
        self.noBackward = True
        self.__renameParams()

    def __renameParams(self):
        return super().__renameParams()

    def computeForward(self, stateVars: dict):
        return super().computeForward(stateVars)

    def computeBackward(self, stateVars: dict):
        return super().computeBackward(stateVars)

    def getEqHeaderStr(self, index):
        return " => {backward} :R{i}".format(backward=self.bs[0], i=index)

    def getForwardEqStr(self, index):
        return "Ksyn{i}".format(i=index)

    def getBackwardEqStr(self, index):
        return super().getBackwardEqStr(index)

