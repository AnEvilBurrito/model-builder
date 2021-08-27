# a new model definition where it is essentially a wrapper
# for a set of reactions

from src.reactions.MichaelisMentenGeneral import MichaelisMentenGeneral
from .reactions.Reactions import Reactions

class Model: 

    def __init__(self, modelName = "unnamed_model"):

        self.reactions = {}
        self.modelName = modelName

        self.activators = {}
        self.specieFamily = {}
        
        # structure: "specieName": "initial concentration"
        self.species = {}

        # automatic reaction naming
        self.nameIterator = 0

    def nameIter(self) -> str: 

        # always begin from 1

        self.nameIterator += 1 

        return self.modelName + '_' + str(self.nameIterator)

    def setModelName(self, name):

        self.modelName = name

    def setParameter(self, parameterName, newValue):
        
        reactions = list(self.reactions.values())

        for re in reactions:
            for key, name in re.paramNames.items():
                if name == parameterName:
                    re.params[key] = newValue

                    # debug msg
                    print(re.params[key], newValue)
        
    def updateSpecies(self):

        # checks every reaction within the model
        # a O(N) update

        reactions = list(self.reactions.values())

        i = 0 
        while i < len(reactions):
            re = reactions[i]
            for fs in re.fs:
                if fs not in self.species and fs != 'None' and fs != None:
                    self.species[fs] = 0
            
            for bs in re.bs:
                if bs not in self.species and bs != 'None' and bs != None:
                    self.species[bs] = 0
            i += 1

    def specieConc(self, specieNames: list, conc: list):

        assert len(specieNames) == len(conc)

        i = 0 
        while i < len(specieNames):
            s = specieNames[i]
            self.species[s] = conc[i]
            i += 1

    def addReaction(self, reaction: Reactions):

        reactions = list(self.reactions.values())
        dup = False
        for r in reactions:
            if r == reaction:
                dup = True 

        if not dup:  
            reaction.setName(self.nameIter())
            self.reactions[reaction.name] = reaction
            self.updateSpecies()

        else:
            print('Duplicate reaction detected', reaction)

    def findReaction(self, fs=None, bs=None, type=None):

        pass

    def addReaction_d(self, reaction_type, fs, bs):
        pass

    def addStimulator(self, reaction_name, stim, kc=0.1, backward=False):
        
        # NOTE: only reactions with .addStimulator() methods
        # can use this method

        re = self.reactions[reaction_name]
        hasStim = getattr(re, "addStimulator", None)

        if callable(hasStim):
            re.addStimulator(stim, kc, backward)

        else:
            print('WARNING: Reaction specified has no addStimulator() method', reaction_name)
            print(re)

    def addInhibitor(self, reaction_name, inh, ki=0.1, backward=False):
        
        re = self.reactions[reaction_name]
        has = getattr(re, "addInhibitor", None)

        if callable(has):
            re.addInhibitor(inh, ki, backward)

        else:
            print('WARNING: Reaction specified has no addInhibitor() method', reaction_name)
            print(re)

    def addActivation(self, activator: str, conc: float, activationTime: float):

        self.activators[activator] = (activator, conc, activationTime)
        self.species[activator] = 0

    def combine(self, otherModel, modelName = "UnnamedModel"):

        # combines model while avoiding duplicate reactions
        # model combination is really just appending reactions and activations and species together

        newModel = Model(modelName)

        otherReactions = list(otherModel.reactions.values())
        reactions = list(self.reactions.values())

        for r in reactions:
            newModel.addReaction(r)

        for ro in otherReactions:
            newModel.addReaction(ro)

        newModel.activators.update(self.activators)
        newModel.activators.update(otherModel.activators)

        newModel.species.update(self.species)
        newModel.species.update(otherModel.species)

        return newModel

    def __str__(self) -> str:
        
        retStr = ''

        reactions = list(self.reactions.values())

        for r in reactions:
            retStr += str(r)
            retStr += '\n'
        
        return retStr


    def getParamSize(self) -> int:
        
        reactions = list(self.reactions.values())

        size = 0
        for re in reactions:
            size += re.getParamSize()
        
        return size


    def generateTxtbc(self):
        
        txtbc = open("{filename}.txtbc".format(filename=self.modelName), "w")

        ### HEADER

        txtbc.write("********** MODEL NAME\n")
        txtbc.write(self.modelName + "\n")
        txtbc.write("\n")
        txtbc.write("********** MODEL NOTES\n")
        txtbc.write("\n")

        ### Model state information

        txtbc.write("********** MODEL STATE INFORMATION\n")
        txtbc.write("% Initial Conditions\n")
        txtbc.write("\n")

        species = self.species.keys()
        for s in species:
            txtbc.write("{specie}(0) = {conc}\n".format(specie = s, conc = self.species[s]))
        txtbc.write("\n")

        
        # NOTE: deprecated code below, have not deleted for possible later reference

        # families = self.specieFamily.keys()
        # families = list(families)

        # for fam in families:
        #     for member in self.specieFamily[fam]: 
        #         txtbc.write("{specie}(0) = {conc}\n".format(specie = member, conc = self.species[member]))
        #     txtbc.write("\n")


        ### Model parameters

        txtbc.write("********** MODEL PARAMETERS\n")

        reactions = list(self.reactions.values())

        i = 0 
        while i < len(reactions):
            re = reactions[i]
            id_ = i + 1
            re_params = re.paramNames
            names = re_params.keys()
            for n in names:
                toStr = re_params[n] + " = " + str(re.params[n]) + "\n"
                txtbc.write(toStr)
            
            txtbc.write("\n")
            i += 1

        txtbc.write("% Constants\n")
        txtbc.write("\n")

        txtbc.write("% Stimulation Concentration\n")
        for a in self.activators:
            txtbc.write("{s} = {v}\n".format(s=a[0], v=a[1]))
        txtbc.write("\n")

        txtbc.write("% Drug Concentration\n")
        txtbc.write("\n")

        txtbc.write("% Time Variables\n")
        for a in self.activators:
            txtbc.write("{s}_on = {time}\n".format(s=a[0], time=a[2]))
        txtbc.write("\n")

        ### Model variables

        txtbc.write("********** MODEL VARIABLES\n")
        txtbc.write("\n")

        # NOTE: deprecated code below, have not deleted for possible later reference

        # for fam in families:

        #     totalStr = "{familyName}_Total = ".format(familyName=fam)
        #     for member in self.specieFamily[fam]: 
        #         totalStr = totalStr + member + " + "

        #     totalStr = totalStr[:-3]
        #     txtbc.write(totalStr)
        #     txtbc.write("\n")

        txtbc.write("\n")
        for a in self.activators:
            txtbc.write("{s}0 = {s}*piecewiseIQM(1,ge(time,{s}_on),0)\n".format(s=a[0]))

        ### Model reactions

        txtbc.write("********** MODEL REACTIONS\n")

        i = 0 
        while i < len(reactions):
            re = reactions[i]
            id_ = i + 1

            txtbc.write(re.getEqHeaderStr(id_))
            txtbc.write("\n")
            if re.getForwardEqStr() is not None:
                txtbc.write("\tvf = " + re.getForwardEqStr())
                txtbc.write("\n")
            if re.getBackwardEqStr() is not None:
                txtbc.write("\tvr = " + re.getBackwardEqStr())
                txtbc.write("\n")
            
            txtbc.write("\n")
            i += 1

        txtbc.write("********** MODEL FUNCTIONS")
        txtbc.write("\n")
        txtbc.write("\n")
        txtbc.write("\n")

        txtbc.write("********** MODEL EVENTS")
        txtbc.write("\n")
        txtbc.write("\n")
        txtbc.write("\n")
        txtbc.write("\n")

        txtbc.write("********** MODEL MATLAB FUNCTIONS")
        txtbc.write("\n")
        txtbc.write("\n")
        txtbc.write("\n")
        txtbc.write("\n")

        ### END

        txtbc.close()


if __name__ == "__main__":
    pass

