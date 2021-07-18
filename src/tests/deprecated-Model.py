from reactions.Reactions import Reactions

class Model: 

    def __init__(self):

        self.species = {}
        self.specieFamily = {}
        self.params = []
        self.reactions = []
        self.modelName = ""
        self.activators = []

    def setModelName(self, name):

        self.modelName = name

    def addSpecie(self, specieName: str, initConc, family: str = "Null"):

        self.species[specieName] = initConc 

        if family is not None:
            if family in self.specieFamily:
                self.specieFamily[family].append(specieName)
            else:
                self.specieFamily[family] = []
                self.specieFamily[family].append(specieName)


    def getSpecieNames(self):

        return list(self.species.keys())

    def getInitConc(self):

        return list(self.species.values())

    def addReaction(self, reaction: Reactions):

        self.reactions.append(reaction)

    def addActivation(self, activator: str, conc: float, activationTime: float):

        self.activators.append((activator, conc, activationTime))

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

        families = self.specieFamily.keys()
        families = list(families)

        for fam in families:
            for member in self.specieFamily[fam]: 
                txtbc.write("{specie}(0) = {conc}\n".format(specie = member, conc = self.species[member]))
            txtbc.write("\n")


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

        for fam in families:

            totalStr = "{familyName}_Total = ".format(familyName=fam)
            for member in self.specieFamily[fam]: 
                totalStr = totalStr + member + " + "

            totalStr = totalStr[:-3]
            txtbc.write(totalStr)
            txtbc.write("\n")

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



    def _diff(self, P, t, *args):
        
        # Given a vector (python list) P and time t,
        # return another vector (python list) using reaction rules

        # specNames = specieNames
        # reactions = reactions

        specieNames = self.getSpecieNames()

        # print(args[0])

        # print(args[1])

        # P is aligned with the order of specieNames

        # retVector = np.zeros(len(specieNames)) 

        # for re in self.reactions:

        #     if re.type == "MichaelisMenten":

        #         # print(re.fs)

        #         forw = specieNames.index(re.fs) 
        #         back = specieNames.index(re.bs)

        #         retVector[forw] -= re.computeForward([P[forw]])
        #         retVector[forw] += re.computeBackward([P[back]])

        #         retVector[back] -= re.computeBackward([P[back]])
        #         retVector[back] += re.computeForward([P[forw]])



        #     if re.type == "MassAction":
                
        #         forw1 = specieNames.index(re.fs[0]) 
        #         forw2 = specieNames.index(re.fs[1]) 
        #         back = specieNames.index(re.bs)

        #         forwVals = [P[forw1], P[forw2]] 
        #         backVals = [P[back]]


        #         retVector[forw1] -= re.computeForward(forwVals)
        #         retVector[forw1] += re.computeBackward(backVals)

        #         retVector[forw2] -= re.computeForward(forwVals)
        #         retVector[forw2] += re.computeBackward(backVals)

        #         retVector[back] -= re.computeBackward(backVals)
        #         retVector[back] += re.computeForward(forwVals)
                

        # return retVector

    def simulate(self, P, t):

        pass
