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
print(ma.fs, ma.bs)
print(ma.params)
print(ma.paramNames)


mm = MichaelisMenten('Erk', 'pErk')
print(mm.fs, mm.bs)
print(mm.params)
print(mm.paramNames)

print(mm.getBackwardEqStr(), mm.getForwardEqStr())

r = MichaelisMentenGeneral("A", "B")
r.addStimulator("C")
r.addStimulator("D")
r.addInhibitor("I", backward=True)
r.addInhibitor("I2", backward=True)
print(r.getForwardEqStr())
print(r.getBackwardEqStr())
print(r.getParams())

### testing model generation of .txtbc files

test = Model('test')
test.addReaction(ma)
test.addReaction(mm)
test.addReaction(r)

test.generateTxtbc()
