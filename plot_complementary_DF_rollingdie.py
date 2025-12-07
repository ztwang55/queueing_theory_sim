import numpy as np
import math
import matplotlib.pyplot as plt
"""
plt.figure(figsize=(10, 6))
x=np.linspace(1,6,6)
y=[1/6 for i in x]
plt.scatter(x,y)
#count, bins, ignored = plt.hist(x, bins=100, density=True, alpha=0.7, color='lightblue', edgecolor='black', label='Probability function')
plt.title('Probability function')
plt.xlabel('outcome of the toss')
plt.ylabel('probabbility')
plt.legend()
plt.xlim(0, 7) 
plt.grid(True, alpha=0.3)
plt.show()
"""
'''
plt.figure(figsize=(10, 6))
x=np.linspace(0,8,100000)
y=[0 if (i<1) else (1/6*math.floor(i) if (i<6) else 1) for i in x]
plt.plot(x,y)
plt.title('CDF')
plt.xlabel('x')
plt.ylabel('probabbility')
plt.legend()
plt.xlim(0, 8) 
plt.grid(True, alpha=0.3)
plt.show()
'''
plt.figure(figsize=(10, 6))
x=np.linspace(0,8,100000)
y=[0 if (i<1) else (1/6*math.floor(i) if (i<6) else 1) for i in x]
z=[1-i for i in y]
plt.plot(x,z)
plt.title('Complementary DF')
plt.xlabel('x')
plt.ylabel('probabbility')
plt.legend()
plt.xlim(0, 8) 
plt.grid(True, alpha=0.3)
plt.show()