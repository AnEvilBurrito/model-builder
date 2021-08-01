
import numpy as np 
from src.Model import Model

class OdeModel(Model):

    def __init__(self, modelName):
        super().__init__(modelName=modelName)

    def _diff(self, P, t):

        # Given a vector (python list) P and time t,
        # return another vector (python list) using reaction rules

        # specNames = specieNames
        # reactions = reactions

        specieNames = self.getSpecieNames()

        # P is aligned with the order of specieNames

        retVector = np.zeros(len(specieNames))

        pass
