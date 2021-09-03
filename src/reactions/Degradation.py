from .Reactions import Reactions

class Degradation(Reactions):

    # Vanilla degradation law without stimulators and inhibitors

    def __init__(self, forwardSpecies, KDeg: float = 0.01):
        super().__init__(forwardSpecies, [])
        self.KDeg = KDeg
        self.stimulators = []

        self.params = {
            'kdeg': KDeg
        }

        self.__renameParams()

    def __renameParams(self):
        
        self.paramNames['kdeg'] = "kdeg_{f1}".format(f1=self.fs[0]) 

    def computeForward(self, stateVars: dict):
        return self.params['kdeg'] * stateVars[self.fs[0]]

    def computeBackward(self, stateVars: dict):
        return super().computeForward(stateVars)

    # def addStimulator(self, specie: str, alpha: float = 0.1):
        
    #     self.stimulators.append((specie, alpha))

    def getEqHeaderStr(self, index):
        return "{forward} => :R{i}".format(forward=self.fs[0], i=index)

    def getForwardEqStr(self):

        return "{kdeg} * {fs}".format(kdeg=self.paramNames['kdeg'], fs=self.fs[0])

        # retStr = "Kdeg{i} * {fs}".format(i=index, fs=self.fs[0])

        # if len(self.stimulators) == 0:
        # return "Kdeg{i} * {fs}".format(i=index, fs=self.fs[0])

        # addi = " * (1 + "
        # i = 0 
        # while i < len(self.stimulators):
        #     st = self.stimulators[i]
        #     specie = st[0]
        #     addiEq = "(alpha{i}b{ai} * {st})".format(i=index, ai=str(i+1), st=specie)
        #     addi = addi + addiEq
        #     i += 1
        #     if i != len(self.stimulators):
        #         addi += " + "
        # addi += ")"

        # return retStr + addi

    def getBackwardEqStr(self):
        return super().getBackwardEqStr()


if __name__ == "__main__":

    r = Degradation("A")
    r.addStimulator("C")
    r.addStimulator("D")

    print(r.getBackwardEqStr(1))
    print(r.getParams(1))
