# importing the required module
import math

import matplotlib.pyplot as plt
import random

Unit_level = 500 * 1.1 * 5
Dist = 7
Fatigue = 1
Moral = 10
x = []
y = []
"""for d in range(1, 10):
    influence_moralfatigue = int( math.sqrt((Moral - Fatigue) ** 2 + (Fatigue - Moral) ** 2))
    influence_distance = random.randint(20, 40 + influence_moralfatigue) * math.exp(-d / 7)
    influence_skill = (0.1 / d ** (1.15 * random.random())) * math.exp(math.log10(Unit_level))
    x.append(d)
    y.append( 1+2/d**2 )
    #y.append(7 + influence_distance + influence_skill - influence_moralfatigue / 3)
# naming the x axis"""

for d in range(1, 10):
    touche = random.randint(0, 10) / d
    x.append(d)
    y.append( touche )
    #y.append(7 + influence_distance + influence_skill - influence_moralfatigue / 3)
plt.xlabel('Distance en blocs de la cible')
# naming the y axis
plt.ylabel('Dommages')
plt.plot(x, y)
plt.show()
