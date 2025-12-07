import numpy as np
from scipy import stats
import pandas as pd

def method_ch8(lambd, mu, k, simulation_time=100000):
    Q = 0
    N_a = 0.0
    N_b = 0.0
    while N_a<simulation_time:
        R = np.random.random()
        arrival_prob = lambd/(lambd+Q*mu)
        if R <= arrival_prob:
            N_a = N_a + 1
            if Q == k:
                N_b = N_b + 1
            else:
                Q = Q + 1
        else:
            Q = Q - 1
    return N_b/N_a

def multiple_runs(method_func, lambd, mu, k, num_runs=30, simulation_time=10000):
    results = []
    for i in range(num_runs):
        np.random.seed(i)
        eq = method_func(lambd, mu, k, simulation_time)
        results.append(eq)
    results = np.array(results)
    mean_pb = np.mean(results)
    std_pb = np.std(results, ddof=1)  
    t_value = stats.t.ppf(0.975, num_runs - 1)  
    margin_of_error = t_value * std_pb / np.sqrt(num_runs)
    ci_lower = mean_pb - margin_of_error
    ci_upper = mean_pb + margin_of_error
    return {
        'mean': mean_pb,
        'std': std_pb,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'ci_width': ci_upper - ci_lower,
        'all_results': results
    }

lambda_p = 39.0
mu_p = 2.0
k_p = 0
num_runs = 30
simulation_time = 10000
print(f"λ={lambda_p}, μ={mu_p}, k={k_p}")
print("Simulation times: ",simulation_time)
print("Num of simulations: ",num_runs)
print()

result1 = multiple_runs(method_ch8, lambda_p, mu_p, k_p, num_runs, simulation_time)
print("Method1 Ch8 simulation:")
print(f"  Pb = {result1['mean']:.6f}")
print(f"  Standard variance = {result1['std']:.6f}")
print(f"  95% Confidence interval = [{result1['ci_lower']:.6f}, {result1['ci_upper']:.6f}]")
print(f"  Confidence interval width = {result1['ci_width']:.6f}")

df = pd.read_excel(r"./erlang.xlsx", engine='openpyxl')
var1 = df['Blocking Probability using recursion']
simulation_mean = []
simulation_ci_lower = []
simulation_ci_upper = []
simulation_recursion = []
for i,k_v in enumerate(var1):
    resultk = multiple_runs(method_ch8, lambda_p, mu_p, i, num_runs, simulation_time)
    simulation_mean.append(resultk['mean'])
    simulation_ci_lower.append(resultk['ci_lower'])
    simulation_ci_upper.append(resultk['ci_upper'])
    if k_v>=resultk['ci_lower'] and k_v<= resultk['ci_upper']:
        simulation_recursion.append(True)
    else:
        simulation_recursion.append(False)
df['Blocking Probability using simulation'] = simulation_mean
df['Confidence interval lower bound'] = simulation_ci_lower
df['Confidence interval upper bound'] = simulation_ci_upper
df['Recursion result in simulation C.I'] = simulation_recursion

df.to_excel(r"./erlang_updated.xlsx", index=False, engine='openpyxl')
