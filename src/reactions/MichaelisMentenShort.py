import numpy as np 
from .MichaelisMentenGeneral import MichaelisMentenGeneral

class MichaelisMentenShort(MichaelisMentenGeneral):

    def __init__(self, forwardSpecie: str, backwardSpecie: str, name, Vmax_f: float, Km_b: float, Vmax_b: float, Km_f: float, noBackward):
        super().__init__(forwardSpecie, backwardSpecie, name=name, Vmax_f=Vmax_f, Km_b=Km_b, Vmax_b=Vmax_b, Km_f=Km_f, noBackward=noBackward)