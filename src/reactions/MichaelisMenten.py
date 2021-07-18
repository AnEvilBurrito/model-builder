from .Reactions import Reactions

class MichaelisMenten(Reactions):

    def __init__(self, forwardSpecie: str, backwardSpecie: str, Vmax_f: float = 10, Km_b: float = 100, Vmax_b: float = 10, Km_f: float = 100):

        super().__init__(forwardSpecie, backwardSpecie)
        self.Vmax_f = Vmax_f
        self.Km_f = Km_f 
        self.Vmax_b = Vmax_b
        self.Km_b = Km_b
        self.type = "MichaelisMenten"

    def computeForward(self, forwardValues: list):

        return (self.Vmax_f * forwardValues[0]) / (self.Km_f + forwardValues[0])

    def computeBackward(self, backwardValues: list):

        return (self.Vmax_b * backwardValues[0]) / (self.Km_b + backwardValues[0])

    def getEqHeaderStr(self, index):
        return "{forward} <=> {backward} :R{i}".format(forward=self.fs[0], backward=self.bs[0], i=index)

    def getForwardEqStr(self, index):
        
        return "Vmax{id}f * {fs} / (Km{id}f + {fs})".format(id=str(index), fs=self.fs[0])

    def getBackwardEqStr(self, index):
        
        return "Vmax{id}b * {bs} / (Km{id}b + {bs})".format(id=str(index), bs=self.bs[0])

    def getParams(self, index):

        return {"Vmax{id}f".format(id=index): self.Vmax_f, "Vmax{id}b".format(id=index): self.Vmax_b, "Km{id}f".format(id=index): self.Km_f, "Km{id}b".format(id=index): self.Km_b}
