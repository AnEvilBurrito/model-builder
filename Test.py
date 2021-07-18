from src.Model import Model
from src.reactions.MassAction import MassAction
from src.reactions.MichaelisMentenGeneral import MichaelisMentenGeneral

### INTEGRATING TWO SEPARATE MODELS

model1 = Model('combine_test')
model2 = Model()

model1.addReaction(MassAction('A', 'B', 'C'))


model2.addReaction(MassAction('A', 'B', 'C'))
model2.addReaction(MichaelisMentenGeneral('C', 'D'))

combined = model1.combine(model2)





