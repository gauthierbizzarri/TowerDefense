# importing the required module
import math

import matplotlib.pyplot as plt
import random

Unit_level = 500 * 1.1 * 5
Dist = 7
Fatigue = 10
Moral = 1
x = []
y = []
for d in range(1, 50):
    influence_moralfatigue = int( math.sqrt((Moral - Fatigue) ** 2 + (Fatigue - Moral) ** 2))
    influence_distance = random.randint(20, 20 + influence_moralfatigue) * math.exp(-d / 7)
    influence_skill = (0.1 / d ** (1.15 * random.random())) * math.exp(math.log10(Unit_level))
    x.append(d)
    y.append(7+
        influence_distance+ influence_skill-influence_moralfatigue/3)
# naming the x axis
plt.xlabel('Distance en blocs')
# naming the y axis
plt.ylabel('Dommages')
plt.plot(x, y)
plt.show()
