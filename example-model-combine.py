import numpy as np
from src.OdeModel import OdeModel
import src.reactions as re

# PPI_Motif1 = OdeModel('PPI_1')

# PPI_Motif1.addReaction(re.MassAction('A', 'P'))

# PPI_Motif1.specieConc(['A', 'P'], [100, 100])

# PPI_Motif2 = OdeModel('PPI_2')
# PPI_Motif2.addReaction(re.MassAction('B', 'P'))

# PPI_Motif2.specieConc(['B', 'P'], [100, 100])


# coupled_PPI = PPI_Motif1.combine(PPI_Motif2, 'Coupled_PPI')
# coupled_PPI.simulate_beta(200)
# coupled_PPI.plot()


# forwardOnly = OdeModel('f')
# forwardOnly.addReaction(re.MichaelisMentenGeneral('A', 'B',noBackward=True))
# forwardOnly.addReaction(re.Synthesis('A'))
# forwardOnly.addReaction(re.Degradation('A'))
# forwardOnly.addReaction(re.Degradation('B'))
# forwardOnly.specieConc(['A'],[100])
# forwardOnly.simulate_beta(10)
# forwardOnly.plot()