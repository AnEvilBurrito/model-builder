import numpy as np
from src.OdeModel import OdeModel
from src.reactions.MichaelisMenten import MichaelisMenten
from src.Model import Model
from src.reactions.MassAction import MassAction
from src.reactions.MichaelisMentenGeneral import MichaelisMentenGeneral
from src.reactions.MichaelisMenten import MichaelisMenten

### INTEGRATING TWO SEPARATE MODELS

# model1 = Model('combine_test')
# model2 = Model()

# model1.addReaction(MassAction('A', 'B', 'C'))


# model2.addReaction(MassAction('A', 'B', 'C'))
# model2.addReaction(MichaelisMentenGeneral('C', 'D'))

# combined = model1.combine(model2)



### Testing MA and Michaelean in refactor

ma = MassAction('Sos', 'Grb2')
# print(ma.fs, ma.bs)
# print(ma.params)
# print(ma.paramNames)

# print(' '.join(ma.fs))

mm = MichaelisMentenGeneral('Erk', 'pErk')
mm.addStimulator('S')
# print(mm.fs, mm.bs)
# print(mm.params)
# print(mm.paramNames)

# print(mm.getBackwardEqStr(), mm.getForwardEqStr())

r = MichaelisMentenGeneral("A", "B")
# r.addStimulator("pErk", kc=1)
# r.addStimulator("D")
# r.addInhibitor("I", backward=True)
# r.addInhibitor("I2", backward=True)
# print(r.getForwardEqStr())
# print(r.getBackwardEqStr())
# print(r.getParams())
# print(r)

# print(''.join(r.fs))

# str1 = ''.join(list1)

### testing model generation of .txtbc files

# test = Model('test')
# test.addReaction(ma)
# test.addReaction(mm)
# test.addReaction(r)

# test.generateTxtbc()

### Testing ODEModel

test_ode = OdeModel('test')
test_ode.addReaction(ma)
test_ode.addReaction(mm)
test_ode.addReaction(r)

test_ode.addStimulator('test_3', "pErk", kc=0.001)

print(test_ode)


test_ode.addActivation('S', 8, 100)
# # test_ode.addActivation('S2', 8, 10)

initSpecies = ['Erk', 'A']
inits = [100] * len(initSpecies)

test_ode.specieConc(initSpecies, inits)

sim_time = 200
# stepsize = 1
# t = np.linspace(0, sim_time, sim_time/stepsize+1)

# # print(t.shape)
# # print(t)

# test_ode.simulate(t, plot=True)

test_ode.simulate_beta(sim_time)
test_ode.plot()

### Testing for new format

# Reactions 



# Network links



