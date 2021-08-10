
# Reaction Interface

class Reactions:

    def __init__(self, forwardSpecies, backwardSpecies, name=''):

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
        self.params = {}
        self.paramNames = {}

        self.noBackward = False

        # used to perform reaction look up in models
        # should be unique
        self.name = name

    def setName(self, newName):

        self.name = newName

    def __str__(self) -> str:
        
        return 'name: ' + self.name + ' | forward specie(s): ' +  ' '.join(self.fs) + ' | backward specie(s): ' + ' '.join(self.bs) + ' | type: ' + type(self).__name__

    def __renameParams(self):
        
        # This function will be called at initialisation or 
        # parameter name update to calibrate parameter names 
        # to a naming rule

        return None

    def computeForward(self, stateVars: dict):
        
        return 0

    def computeBackward(self, stateVars: dict):

        return 0

    # To generate txtbc

    def getEqHeaderStr(self, index):

        return None

    def getForwardEqStr(self):

        return None

    def getBackwardEqStr(self):

        return None

    # ^--- To generate txtbc

    def getParams(self):

        return self.params

    def getParamSize(self):

        return len(self.params)

    def __eq__(self, o: object) -> bool:
        
        same_fs = False
        if self.fs == o.fs:
            same_fs = True 

        same_bs = False
        if self.bs == o.bs:
            same_bs = True

        return (same_bs and same_fs)
