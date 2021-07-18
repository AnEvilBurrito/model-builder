from .Reactions import Reactions

class MassAction(Reactions):

    # Simplified Mass Action with only two forward specie and one backward specie,
    # with molecularities of 1

    def __init__(self, forwardSpecie1: str, forwardSpecie2: str, backwardSpecie: str, Ka: float = 0.001, Kd: float = 0.01):

        super().__init__([forwardSpecie1, forwardSpecie2], backwardSpecie)
        self.Ka = Ka
        self.Kd = Kd
        self.type = "MassAction"

    def computeForward(self, forwardValues: list):

        forwardSpecie1 = forwardValues[0]
        forwardSpecie2 = forwardValues[1]

        return self.Ka * forwardSpecie1 * forwardSpecie2

    def computeBackward(self, backwardValues: list):

        backwardSpecie = backwardValues[0]

        return self.Kd * backwardSpecie

    def getEqHeaderStr(self, index):
        return "{forward1} + {forward2} <=> {backward} :R{i}".format(forward1=self.fs[0], forward2=self.fs[1], backward=self.bs[0], i=index)

    def getForwardEqStr(self, index):
        
        return "Ka{i} * {fs1} * {fs2}".format(i=index, fs1=self.fs[0], fs2=self.fs[1])

    def getBackwardEqStr(self, index):
        
        return "Kd{i} * {bs}".format(i=index, bs=self.bs[0])

    def getParams(self, index):

        return {"Ka{id}".format(id=index): self.Ka, "Kd{id}".format(id=index): self.Kd}
