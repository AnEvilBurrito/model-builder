from .Reactions import Reactions

class Synthesis(Reactions):

    def __init__(self, backwardSpecies, KSyn: float = 0.01):
        super().__init__("None", backwardSpecies)
        self.KSyn = KSyn

    def getEqHeaderStr(self, index):
        return " => {backward} :R{i}".format(backward=self.bs[0], i=index)

    def getForwardEqStr(self, index):
        return "Ksyn{i}".format(i=index)

    def getBackwardEqStr(self, index):
        return super().getBackwardEqStr(index)

    def getParams(self, index):
        return {"Ksyn{i}".format(i=index): self.KSyn}

