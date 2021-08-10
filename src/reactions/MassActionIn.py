from .MassAction import MassAction
from .Inhibitor import Inhibitor
import numpy as np 

class MassActionIn(MassAction, Inhibitor):

    def __init__(self, forwardSpecie1: str, forwardSpecie2: str, backwardSpecie: str, name, Ka: float, Kd: float):
        super().__init__(forwardSpecie1, forwardSpecie2, backwardSpecie=backwardSpecie, name=name, Ka=Ka, Kd=Kd)

        self.Inh = []