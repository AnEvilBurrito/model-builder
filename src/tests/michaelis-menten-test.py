# Produce 'Flattening the curve' graphs using SIR model

from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


# Vanilla model of 'michaelis-menten'

# isolate 2 individual for every 1 infected

Vmaxf1 = 10
Vmaxb1 = 10
Vmaxf2 = 10
Vmaxb2 = 10
Kmf1 = 100
Kmb1 = 100
Kmf2 = 100
Kmb2 = 100

t = np.linspace(0, 200, 200*100)

initial_p = np.array([0,100,1])


def diff(P, t, vm1, vm2, vm3, vm4, km1, km2, km3, km4):
    uEGFR, EGFR, pEGFR = P[0], P[1], P[2]
    vf1 = (vm1 * uEGFR) / (km1 + uEGFR) 
    vb1 = (vm2 * EGFR) / (km2 + EGFR)
    vf2 = (vm3 * 2 * EGFR) / (km3 + EGFR)
    vb2 = (vm4 * pEGFR) / (km4 + pEGFR)
    


    return np.array([vb1 - vf1, 
                    vf1 - vb1 - vf2 + vb2,
                    vf2 - vb2])


P = odeint(diff, initial_p, t, args=(Vmaxf1, Vmaxb1, Vmaxf2, Vmaxb2, Kmf1, Kmb1, Kmf2, Kmb2))

uEGFRarr, EGFRarr, pEGFRarr = P.T

plt.plot(t, uEGFRarr, label="uEGFR")
plt.plot(t, EGFRarr, label="EGFR")
plt.plot(t, pEGFRarr, label="pEGFR")



plt.grid()
plt.legend()
plt.show()

