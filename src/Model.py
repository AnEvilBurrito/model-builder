# a new model definition where it is essentially a wrapper
# for a set of reactions

from .reactions.Reactions import Reactions

class Model: 

    def __init__(self, modelName = "unnamed_model"):

        self.reactions = []
        self.modelName = modelName

        # structure: "specieName": "initial concentration"
        self.activators = []
        self.specieFamily = {}
        self.species = {}

    def setModelName(self, name):

        self.modelName = name

    def updateSpecies(self):

        # checks every reaction within the model
        # a O(N) update

        i = 0 
        while i < len(self.reactions):
            re = self.reactions[i]
            for fs in re.fs:
                if fs not in self.species and fs != 'None' and fs != None:
                    self.species[fs] = 100
            
            for bs in re.bs:
                if bs not in self.species and bs != 'None' and bs != None:
                    self.species[bs] = 100
            i += 1

    def specieConc(self, specieNames: list, conc: list):

        assert len(specieNames) == len(conc)

        i = 0 
        while i < len(specieNames):
            s = specieNames[i]
            self.species[s] = conc[i]
            i += 1

    def addReaction(self, reaction: Reactions):

        dup = False
        for r in self.reactions:
            if r == reaction:
                dup = True 

        if not dup:  
            self.reactions.append(reaction)
            self.updateSpecies()

        else:
            print('Duplicate reaction detected', reaction)

    def addActivation(self, activator: str, conc: float, activationTime: float):

        self.activators.append((activator, conc, activationTime))

    def combine(self, otherModel, modelName = "None"):

        # combines model while avoiding duplicate reactions
        # model combination is really just appending reactions and activations together

        newModel = Model(modelName)

        otherReactions = otherModel.reactions
        reactions = self.reactions

        for r in reactions:
            newModel.addReaction(r)

        for ro in otherReactions:
            newModel.addReaction(ro)

        return newModel

    def __str__(self) -> str:
        pass

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

        i = 0 
        while i < len(self.reactions):
            re = self.reactions[i]
            id_ = i + 1
            re_params = re.getParams(id_)
            names = re_params.keys()
            for n in names:
                toStr = n + " = " + str(re_params[n]) + "\n"
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
        while i < len(self.reactions):
            re = self.reactions[i]
            id_ = i + 1

            txtbc.write(re.getEqHeaderStr(id_))
            txtbc.write("\n")
            if re.getForwardEqStr(id_) is not None:
                txtbc.write("\tvf = " + re.getForwardEqStr(id_))
                txtbc.write("\n")
            if re.getBackwardEqStr(id_) is not None:
                txtbc.write("\tvr = " + re.getBackwardEqStr(id_))
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

