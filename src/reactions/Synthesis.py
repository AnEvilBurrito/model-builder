from src.reactions.Inhibitor import Inhibitor
from .Reactions import Reactions
from .Inhibitor import Inhibitor
import numpy as np

class Synthesis(Reactions, Inhibitor):

    def __init__(self, backwardSpecies, KSyn: float = 0.01):

        # implements constitutive synthesis

        super().__init__([], backwardSpecies)
        Inhibitor.__init__(self)

        self.type = 'Syn'
        self.params = {
            'ksyn': KSyn
        }
        
        self.noBackward = True
        self.__renameParams()


    def __renameParams(self):
        
        self.paramNames['ksyn'] = "Vsyn_{bs}".format(bs=self.bs[0])

        if len(self.fInh) != 0:
            for inh in self.fInh:
                str_ = "Ki_syn_{bs}_{inh}".format(bs=self.bs[0], inh=inh)
                self.paramNames['kif_' + inh] = str_ 

    def addInhibitor(self, specie: str, ki: float = 0.01, backward=True):
        
        self.addInhibitor_list(specie=specie, ki=ki, backward=backward)
        self.__renameParams()

    def computeForward(self, stateVars: dict):

        if len(self.fInh) == 0:
            return self.params['ksyn']


        ki_product = []


        # for ki_state in self.Inh:
        #     p = 1 + (stateVars[ki_state] * self.params['ki_' + ki_state])
        #     ki_product.append(p)

        top = self.params['ksyn']
        bot = self.ki_compute(stateVars=stateVars, forward=True)
        # bot = np.prod(ki_product) 

        return top/bot
        
    def computeBackward(self, stateVars: dict):
        return super().computeBackward(stateVars)

    def getEqHeaderStr(self, index):
        return " => {backward} :R{i}".format(backward=self.bs[0], i=index)

    def getForwardEqStr(self):

        if len(self.fInh) == 0:
            return "Ksyn_{i}".format(i=self.bs[0])

        top = "Ksyn_{i}".format(i=self.bs[0])
        bot = self.ki_str(forward=True)
        # bot = ""

        # i = 0 
        # while i < len(self.Inh):
        #     In = self.Inh[i][0]
        #     bot = bot + "(1 + {In} * {ki}) * ".format(In=In, ki=self.paramNames['ki_' + In])
        #     i += 1
        # bot = bot[:-3]             

        retStr = top + " / " + bot
        return retStr

    def getBackwardEqStr(self):
        return super().getBackwardEqStr()

