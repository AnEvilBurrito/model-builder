from .MichaelisMenten import MichaelisMenten


class MichaelisMentenGeneral(MichaelisMenten):

    def __init__(self, forwardSpecie: str, backwardSpecie: str, Vmax_f: float = 10, Km_b: float = 100, Vmax_b: float = 10, Km_f: float = 100, noForward=False, noBackward=False):

        # Generalised forward Michaelis Menten kinetics
        # incorporates stimulation and inhibition
        # need to include kinetic constant values for each stimulator/inhibitor
        # Assumption: each stimulator/inhibitor is independent!
        # NOTE: currently, this class assumes allosteric inhibition 

        super().__init__(forwardSpecie, backwardSpecie, Vmax_f=Vmax_f, Km_b=Km_b, Vmax_b=Vmax_b, Km_f=Km_f)
        self.type = "MG"
        
        self.stimulatorsForward = []
        self.inhibitorsForward = []

        self.stimulatorsBackward = []
        self.inhibitorsBackward = []

        self.noForward = noForward
        self.noBackward = noBackward

    def addStimulator(self, specie: str, kc: float = 0.1, backward=False):

        if backward:
            self.stimulatorsBackward.append((specie, kc))
        else:    
            self.stimulatorsForward.append((specie, kc))

    def addInhibitor(self, specie: str, ki: float = 0.01, backward=False):

        if backward:
            self.inhibitorsBackward.append((specie, ki))
        else:
            self.inhibitorsForward.append((specie, ki))

    def computeForward(self, forwardValues: list):

        # NOTE: not utilised

        return super().computeForward(forwardValues)

        
    def computeBackward(self, backwardValues: list):
        
        # NOTE: not utilised 

        return super().computeBackward(backwardValues)

    def getEqHeaderStr(self, index):
        if self.noBackward:
            return "{forward} => {backward} :R{i}".format(forward=self.fs[0], backward=self.bs[0], i=index)
        return super().getEqHeaderStr(index)

    def getForwardEqStr(self, index):

        if self.noForward:
            return None

        if len(self.stimulatorsForward) == 0 and len(self.inhibitorsForward) == 0:
            return super().getForwardEqStr(index)

        retStr = ""
        top = ""
        bot = ""

        top += "("
        if len(self.stimulatorsForward) == 0:
            top += "Vmax{id}f".format(id=index)
        else:
            i = 0 
            while i < len(self.stimulatorsForward):
                st = self.stimulatorsForward[i][0]
                top = top + "Kc{id}f{kc_id} * {st} + ".format(id=index, kc_id=str(i+1), st=st)
                i += 1  
            top = top[:-3]
        top += ")"
        top += " * {fs}".format(fs=self.fs[0])

        bot = "(Km{id}f + {fs}) * ".format(id=index, fs=self.fs[0])
        i = 0
        while i < len(self.inhibitorsForward):
            In = self.inhibitorsForward[i][0]
            bot = bot + "(1 + {In} / Ki{id}f{ki_id}) * ".format(In=In, id=index, ki_id=str(i+1))
            i += 1
        bot = bot[:-3]             

        retStr = top + " / " + bot
        return retStr

    def getBackwardEqStr(self, index):

        if self.noBackward:
            return None

        if len(self.stimulatorsBackward) == 0 and len(self.inhibitorsBackward) == 0:
            return super().getBackwardEqStr(index)

        retStr = ""
        top = ""
        bot = ""

        top += "("
        if len(self.stimulatorsBackward) == 0:
            top += "Vmax{id}b".format(id=index)
        else:
            i = 0 
            while i < len(self.stimulatorsBackward):
                st = self.stimulatorsBackward[i][0]
                top = top + "Kc{id}b{kc_id} * {st} + ".format(id=index, kc_id=str(i+1), st=st)
                i += 1  
            top = top[:-3]
        top += ")"
        top += " * {bs}".format(bs=self.bs[0])

        bot = "(Km{id}f + {bs}) * ".format(id=index, bs=self.bs[0])
        i = 0
        while i < len(self.inhibitorsBackward):
            In = self.inhibitorsBackward[i][0]
            bot = bot + "(1 + {In} / Ki{id}f{ki_id}) * ".format(In=In, id=index, ki_id=str(i+1))
            i += 1
        bot = bot[:-3]             

        retStr = top + " / " + bot


        return retStr


    def getParams(self, index):


        all_params = {}

        if len(self.stimulatorsForward) == 0:
            # return Vmaxf
            vmax_str = "Vmax{id}f".format(id=index)
            all_params[vmax_str] = self.Vmax_f

        if len(self.stimulatorsBackward) == 0:
            # return Vmaxb 
            vmax_str = "Vmax{id}b".format(id=index)
            all_params[vmax_str] = self.Vmax_b
        
        kmf_str = "Km{id}f".format(id=index)
        Kmb_str = "Km{id}b".format(id=index)
        all_params[kmf_str] = self.Km_f
        all_params[Kmb_str] = self.Km_b
        # NOTE: REALLY SHOULD REFACTOR

        i = 0 
        while i < len(self.stimulatorsForward):
            k_str = "Kc{id}f{kc_id}".format(id=index, kc_id=str(i+1))
            all_params[k_str] = self.stimulatorsForward[i][1]
            i += 1

        i = 0
        while i < len(self.stimulatorsBackward):
            k_str = "Kc{id}b{kc_id}".format(id=index, kc_id=str(i+1))
            all_params[k_str] = self.stimulatorsBackward[i][1]
            i += 1

        i = 0
        while i < len(self.inhibitorsForward):
            k_str = "Ki{id}f{ki_id}".format(id=index, ki_id=str(i+1))
            all_params[k_str] = self.inhibitorsForward[i][1]
            i += 1

        i = 0
        while i < len(self.inhibitorsBackward):
            k_str = "Ki{id}f{ki_id}".format(id=index, ki_id=str(i+1))
            all_params[k_str] = self.inhibitorsBackward[i][1]
            i += 1
    
        return all_params


if __name__ == "__main__":
    
    r = MichaelisMentenGeneral("A", "B")
    r.addStimulator("C")
    r.addStimulator("D")
    r.addInhibitor("I", backward=True)
    r.addInhibitor("I2", backward=True)
    print(r.getForwardEqStr(1))
    print(r.getBackwardEqStr(1))
    print(r.getParams(1))
