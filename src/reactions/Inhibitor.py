
import numpy as np


class Inhibitor():

    def __init__(self) -> None:
        # This class implements functions which is generalisable to
        # reactions containing allosteric inhibitors
         
        
        self.fInh = []
        self.bInh = []
    
    def addInhibitor_list(self, specie: str, ki: float = 0.01, backward=False):

        if backward:
            self.params['kib_' + specie] = ki
            self.bInh.append(specie)
        else:
            self.params['kif_' + specie] = ki
            self.fInh.append(specie)

    def ki_compute(self, stateVars: dict, forward):

        if forward:
            inh = self.fInh
            ki_str = 'kif_'
        else:
            inh = self.bInh
            ki_str = 'kib_'

        ki_product = []

        for ki_state in inh:
            p = 1 + (stateVars[ki_state] * self.params[ki_str + ki_state])
            ki_product.append(p)
        
        return np.prod(ki_product)

    def ki_str(self, forward):

        if forward:
            inh = self.fInh
            ki_str = 'kif_'
        else:
            inh = self.bInh
            ki_str = 'kib_'

        bot = ""

        i = 0
        while i < len(inh):
            In = inh[i][0]
            bot = bot + "(1 + {In} * {ki}) * ".format(In=In, ki=self.paramNames[ki_str + In])
            i += 1
        bot = bot[:-3]   

        return bot
