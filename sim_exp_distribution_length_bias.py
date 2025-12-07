import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import poisson

'''
N_t_values = []
lambda_param=2
t_target=2
n_points=10000
n_simulations=10000
for i in range(n_simulations):
    d_i = np.random.exponential(1/lambda_param, n_points)
    t_i = np.cumsum(d_i)
    N_t = np.sum(t_i <= t_target)
    N_t_values.append(N_t)
    
empirical_mean = np.mean(N_t_values)
theoretical_mean = lambda_param * t_target
print(empirical_mean,theoretical_mean)

plt.figure(figsize=(4, 4))
counts, bins, patches = plt.hist(N_t_values, bins=30, density=True, alpha=0.7, 
                                label='Simulation value')
bin_width = bins[1] - bins[0]
x = np.arange(0, max(N_t_values)+1)
plt.plot(x, poisson.pmf(x, theoretical_mean)/bin_width, 'ro-', label='Theoretical value Poisson(λt)')
plt.legend()

plt.tight_layout()
plt.show()
'''

lambda_param=1
n_points=100000
n_simulations=1000
t_target=10000
interval=[]

for i in range(n_simulations):
    x=np.random.uniform(1,10000,1)
    d_i = np.random.exponential(1/lambda_param, n_points)
    t_i = np.cumsum(d_i)
    idx = np.searchsorted(t_i, x)
    left = t_i[idx-1] if idx > 0 else 0
    right = t_i[idx]
    interval_length = right - left
    interval.append(interval_length)
    


empirical_mean = np.mean(interval)
theoretical_mean = 1/lambda_param
print("Empirical mean: ", empirical_mean)
print("Theoretical mean: ", theoretical_mean)
'''
plt.figure(figsize=(4, 4))
counts, bins, patches = plt.hist(N_t_values, bins=30, density=True, alpha=0.7, 
                                label='Simulation value')
bin_width = bins[1] - bins[0]
x = np.arange(0, max(N_t_values)+1)
plt.plot(x, poisson.pmf(x, theoretical_mean)/bin_width, 'ro-', label='Theoretical value Poisson(λt)')
plt.legend()

plt.tight_layout()
plt.show()
'''