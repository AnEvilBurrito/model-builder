
import numpy as np
from numpy.linalg.linalg import solve 
from src.Model import Model
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib as mpl

# mpl.rcParams['figure.dpi'] = 300
# mpl.rc('savefig', dpi=300)

class OdeModel(Model):

    def __init__(self, modelName):
        super().__init__(modelName=modelName)

        self.P = None 
        self.t = None

    def combine(self, otherModel, modelName="UnnamedModel"):

        # combines model while avoiding duplicate reactions
        # model combination is really just appending reactions and activations and species together
        # NOTE: this function is incomplete

        newModel = OdeModel(modelName)

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

    def _diff(self, P, t):

        # Given a vector (python list) P and time t,
        # return another vector (python list) using reaction rules

        # specNames = specieNames
        # reactions = reactions

        # P = specie

        specieNames = list(self.species.keys())

        # P is aligned with the order of specieNames

        P_ = np.zeros(len(specieNames))
        stateVars = dict(zip(specieNames, P))

        # print(type(specieNames))
        
        reactions = list(self.reactions.values())

        for re in reactions:

            for sp in re.fs:

                idx = specieNames.index(sp)
                P_[idx] -= re.computeForward(stateVars)
                P_[idx] += re.computeBackward(stateVars)

            for sp in re.bs:

                idx = specieNames.index(sp)
                P_[idx] -= re.computeBackward(stateVars)
                P_[idx] += re.computeForward(stateVars)

        return P_

    def simulate_nil_act(self, sim_time, stepsize=0.01, plot=False):

        # naive simulation without activation

        t = np.linspace(0, sim_time, sim_time/stepsize+1)
        P = odeint(self._diff, list(self.species.values()), t)

        if plot:
            self.__plot(P.T, t)

        self.P = P.T
        self.t = t

        return P.T

    def simulate_beta(self, sim_time, stepsize=0.01, plot=False):

        # allows for step function activators iteratively performs 
        # odeint instead of simulating everything at once

        activatorVals = list(self.activators.values())

        activatorVals.sort(key=lambda x: x[2])

        # print(activatorVals)

        t = np.linspace(0, sim_time, int(sim_time/stepsize+1))
        remain_time = sim_time

        current_p = list(self.species.values())

        specieNames = list(self.species.keys())

        ret = np.array([current_p])
        
        for tuple_ in activatorVals:
            act, conc, t_a = tuple_[0], tuple_[1], tuple_[2]

            if t_a < remain_time:
                t_s = np.linspace(0, t_a, int(t_a/stepsize+1))
                P = odeint(self._diff, current_p, t_s)

                current_p = P[-1]
                idx = specieNames.index(act)
                current_p[idx] += conc

                # print(ret.shape)
                ret = np.concatenate((ret, P[:-1]))
                # print(P.shape)
            
            remain_time -= t_a

        t_s = np.linspace(0, remain_time, int(remain_time/stepsize+1))
        P = odeint(self._diff, current_p, t_s)

        ret = np.concatenate((ret, P))
        if plot:
            self.__plot(ret[1:].T, t)

        self.P = ret[1:].T 
        self.t = t
        
        return ret[1:].T


    def __plot(self, a, t):

        names = list(self.species.keys())
        i = 0
        while i < len(a):
            plt.plot(t, a[i], label=names[i])
            i += 1
        plt.grid()
        plt.legend()
        plt.show()

    def plot(self, ignore_list=None, colours=None, savefig=False, name='none'):

        if ignore_list is None:
            ignore_list = []
        names = list(self.species.keys())
        ci = 0 
        i = 0
        while i < len(self.P):
            if names[i] not in ignore_list:
                if colours:
                    plt.plot(self.t, self.P[i], label=names[i], c=colours[ci])
                    ci += 1
                else:
                    plt.plot(self.t, self.P[i], label=names[i])
            i += 1
        plt.grid()
        plt.legend()
        plt.xlabel('Time (min)')
        plt.ylabel('Specie level (arb. unit)')
        plt.title(self.modelName)

        if savefig:
            plt.savefig(name, dpi=100)

        plt.show()



    def plotOnly(self, only_print=None, colours=None, savefig=False, name='none'):

        if only_print is None:
            only_print = []
            
        names = list(self.species.keys())
        ci = 0
        i = 0
        while i < len(self.P):
            if names[i] in only_print:
                if colours:
                    plt.plot(self.t, self.P[i], label=names[i], c=colours[ci])
                    ci += 1
                else:
                    plt.plot(self.t, self.P[i], label=names[i])
            i += 1
        plt.grid()
        plt.legend()
        plt.xlabel('Time (min)')
        plt.ylabel('Specie level (unit)')
        plt.title(self.modelName)
        if savefig:
            plt.savefig(name, dpi=100)
        plt.show()


    def extractStateValues(self, stateName):
        
        specieNames = list(self.species.keys())
        idx = specieNames.index(stateName)
        return self.P[idx]


