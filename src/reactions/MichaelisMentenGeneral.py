from .MichaelisMenten import MichaelisMenten
import numpy as np


class MichaelisMentenGeneral(MichaelisMenten):

    def __init__(self, forwardSpecie: str, backwardSpecie: str, Vmax_f: float = 10, Km_b: float = 100, Vmax_b: float = 10, Km_f: float = 100, noBackward=False):

        # Generalised forward Michaelis Menten kinetics
        # incorporates stimulation and inhibition
        # need to include kinetic constant values for each stimulator/inhibitor
        # Assumption: each stimulator/inhibitor is independent!
        # NOTE: currently, this class assumes allosteric inhibition 

        super().__init__(forwardSpecie, backwardSpecie, Vmax_f=Vmax_f, Km_b=Km_b, Vmax_b=Vmax_b, Km_f=Km_f)
        
        self.type = "MG"

        self.noBackward = noBackward

        self.fStim = []
        self.bStim = []
        self.fInh = []
        self.bInh = []

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

        if len(self.fStim) != 0:
            if 'vmaxf' in self.params:
                del self.params['vmaxf']
            if 'vmaxf' in self.paramNames:
                del self.paramNames['vmaxf']

            for stim in self.fStim:
                str_ = 'kc_{fs}_to_{bs}_{st}'.format(fs=self.fs[0], bs=self.bs[0], st=stim)
                self.paramNames['kcf_' + stim] = str_

        if len(self.bStim) != 0:
            if 'vmaxb' in self.params:
                del self.params['vmaxb']
            if 'vmaxb' in self.paramNames:
                del self.paramNames['vmaxb']

            for stim in self.bStim:
                str_ = 'kc_{bs}_to_{fs}_{st}'.format(fs=self.fs[0], bs=self.bs[0], st=stim)
                self.paramNames['kcb_' + stim] = str_

        if len(self.fInh) != 0:
            for stim in self.fInh:
                str_ = 'ki_{fs}_to_{bs}_{st}'.format(fs=self.fs[0], bs=self.bs[0], st=stim)
                self.paramNames['kif_' + stim] = str_

        if len(self.bInh) != 0:
            for stim in self.bInh:
                str_ = 'ki_{bs}_to_{fs}_{st}'.format(fs=self.fs[0], bs=self.bs[0], st=stim)
                self.paramNames['kib_' + stim] = str_


    def addStimulator(self, specie: str, kc: float = 0.1, backward=False):

        if backward:
            self.params['kcb_' + specie] = kc
            self.bStim.append(specie)
        else:
            self.params['kcf_' + specie] = kc 
            self.fStim.append(specie)

        self.__renameParams()

    def addInhibitor(self, specie: str, ki: float = 0.01, backward=False):

        if backward:
            self.params['kib_' + specie] = ki
            self.bInh.append(specie)
        else:
            self.params['kif_' + specie] = ki
            self.fInh.append(specie)
        
        self.__renameParams()

    def __vanilla(self, forward: bool):

        if forward:
            if not self.fStim and not self.fInh:
                return True
            else:
                return False
        else:
            if not self.bInh and not self.bStim:
                return True
            else:
                return False

    def __compute(self, stateVars: dict, forward: bool):

        if forward:
            s = stateVars[self.fs[0]]
            stim = self.fStim
            inh = self.fInh
            kc_str = 'kcf_'
            ki_str = 'kif_'
            km_str = 'kmf'
        else:
            s = stateVars[self.bs[0]]
            stim = self.bStim
            inh = self.bInh
            kc_str = 'kcb_'
            ki_str = 'kib_'
            km_str = 'kmb'

        kc_product = []
        ki_product = []

        for kc_state in stim:
            p = stateVars[kc_state] * self.params[kc_str + kc_state]
            kc_product.append(p)

        for ki_state in inh:
            p = 1 + (stateVars[kc_state] / self.params[ki_str + ki_state])
            ki_product.append(p)

        top = np.sum(kc_product) * s
        bot = np.prod(ki_product) * (self.params[km_str] + s)

        return top / bot


    def computeForward(self, stateVars: dict):

        if self.__vanilla(forward=True):
            return super().computeForward(stateVars)

        return self.__compute(stateVars, forward=True)

    def computeBackward(self, stateVars: dict):

        if self.__vanilla(forward=False):
            return super().computeBackward(stateVars)

        return self.__compute(stateVars, forward=False)

    def getEqHeaderStr(self, index):
        if self.noBackward:
            return "{forward} => {backward} :R{i}".format(forward=self.fs[0], backward=self.bs[0], i=index)
        return super().getEqHeaderStr(index)

    def __getEqStr(self, forward: bool):

        if forward:
            s = self.fs[0]
            stim = self.fStim
            inh = self.fInh
            kc_str = 'kcf_'
            ki_str = 'kif_'
            km_str = 'kmf'
            vmax = 'vmaxf'
        else:
            s = self.bs[0]
            stim = self.bStim
            inh = self.bInh
            kc_str = 'kcb_'
            ki_str = 'kib_'
            km_str = 'kmb'
            vmax = 'vmaxb'

        retStr = ""
        top = ""
        bot = ""

        top += "("
        if len(stim) == 0:
            top += self.paramNames[vmax]
        else:
            i = 0 
            while i < len(stim):
                st = stim[i]
                top = top + "{kc} * {st} + ".format(kc=self.paramNames[kc_str + st], st=st)
                i += 1  
            top = top[:-3]
        top += ")"
        top += " * {s}".format(s=s)

        bot = "({km} + {s}) * ".format(km=self.paramNames[km_str], s=s)
        i = 0
        while i < len(inh):
            In = inh[i][0]
            bot = bot + "(1 + {In} / {ki}) * ".format(In=In, ki=self.paramNames[ki_str + In])
            i += 1
        bot = bot[:-3]             

        retStr = top + " / " + bot
        return retStr

    def getForwardEqStr(self):

        if self.__vanilla(forward=True):
            return super().getForwardEqStr()

        return self.__getEqStr(forward=True)

    def getBackwardEqStr(self):

        if self.noBackward:
            return None

        if self.__vanilla(forward=False):
            return super().getBackwardEqStr()

        return self.__getEqStr(forward=False)


if __name__ == "__main__":
    
    r = MichaelisMentenGeneral("A", "B")
    r.addStimulator("C")
    r.addStimulator("D")
    r.addInhibitor("I", backward=True)
    r.addInhibitor("I2", backward=True)
    print(r.getForwardEqStr(1))
    print(r.getBackwardEqStr(1))
    print(r.getParams(1))
