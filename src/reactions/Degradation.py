from .Reactions import Reactions

class Degradation(Reactions):

    def __init__(self, forwardSpecies, KDeg: float = 0.01):
        super().__init__(forwardSpecies, "None")
        self.KDeg = KDeg
        self.stimulators = []

    def addStimulator(self, specie: str, alpha: float = 0.1):
        
        self.stimulators.append((specie, alpha))

    def getEqHeaderStr(self, index):
        return "{forward} => :R{i}".format(forward=self.fs[0], i=index)

    def getForwardEqStr(self, index):
        retStr = "Kdeg{i} * {fs}".format(i=index, fs=self.fs[0])

        if len(self.stimulators) == 0:
            return "Kdeg{i} * {fs}".format(i=index, fs=self.fs[0])

        addi = " * (1 + "
        i = 0 
        while i < len(self.stimulators):
            st = self.stimulators[i]
            specie = st[0]
            addiEq = "(alpha{i}b{ai} * {st})".format(i=index, ai=str(i+1), st=specie)
            addi = addi + addiEq
            i += 1
            if i != len(self.stimulators):
                addi += " + "
        addi += ")"

        return retStr + addi

    def getBackwardEqStr(self, index):
        return super().getBackwardEqStr(index)

    def getParams(self, index):

        all_params = {"Kdeg{i}".format(i=index): self.KDeg}

        i = 0 
        while i < len(self.stimulators):
            k_str = "alpha{id}b{ai}".format(id=index, ai=str(i+1))
            all_params[k_str] = self.stimulators[i][1]
            i += 1

        return all_params


if __name__ == "__main__":

    r = Degradation("A")
    r.addStimulator("C")
    r.addStimulator("D")

    print(r.getBackwardEqStr(1))
    print(r.getParams(1))
