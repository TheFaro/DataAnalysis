import numpy as np

from matplotlib import pyplot as plt

def sinplot(flip=1):
    x = np.linspace(0,14,100)
    for i in range(1,5):
        plt.plot(x, np.sin(x + i * 0.5) * (7 - i) * flip)


import seaborn as sb
sb.set_style("whitegrid")
sinplot()
sb.despine()
plt.show()