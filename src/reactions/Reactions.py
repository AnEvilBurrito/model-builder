
class Reactions:

    def __init__(self, forwardSpecies, backwardSpecies):

        # forwardSpecies and backwardSpecies can be list or str
        # but are always initialised as list
        if isinstance(forwardSpecies, str):
            self.fs = [forwardSpecies]
        else:
            self.fs = forwardSpecies
        if isinstance(backwardSpecies, str):
            self.bs = [backwardSpecies]
        else: 
            self.bs = backwardSpecies
        self.type = "None"

    def computeForward(self, forwardValues: list):
        
        return None

    def computeBackward(self, backwardValues: list):

        return None

    def getEqHeaderStr(self, index):

        return None

    def getForwardEqStr(self, index):

        return None

    def getBackwardEqStr(self, index):

        return None

    def getParams(self, index):

        return None

    def __eq__(self, o: object) -> bool:
        
        same_fs = False
        if self.fs == o.fs:
            same_fs = True 

        same_bs = False
        if self.bs == o.bs:
            same_bs = True

        return (same_bs and same_fs)