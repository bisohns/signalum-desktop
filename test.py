import numpy as np
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot([1.0,1.5], [100,100], color='r', linestyle='-')
plt.show()