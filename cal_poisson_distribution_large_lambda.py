import os
import math
import csv
from scipy import stats
from scipy.stats import poisson

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'poisson_distribution_large_lambda.csv')

#set parameter: \lambda
lamda = 10000

#set variable range: i
i_max = lamda + 500
i_min = lamda - 500

#set initial value: P(X=0)=exp(-lambda)*1/1 for formula, P(Y=0)=1 for recursion
pxi0=poisson.pmf(lamda, lamda)
pyi0 = 1

#create csv file
f = open(file_path, 'w', encoding='utf-8', newline="")
f_writer = csv.writer(f)
f_writer.writerow(["lambda",lamda])
f_writer.writerow(["i","Poisson distribution formula","Values based on recursion","Normalised values"])

py = {}
py[lamda]=pyi0
py_c = pyi0
for i in range(lamda - 1, i_min - 1, -1):
    py_c = py_c * (i + 1) / lamda
    py[i] = py_c

py_c = pyi0
for i in range(lamda + 1, i_max + 1):
    py_c = py_c * lamda / i
    py[i] = py_c

total_sum = sum(py.values())

for i in range(i_min,i_max+1):
    #p_formula = px0 * math.pow(lamda,i) / math.factorial(i)
    p_formula = stats.poisson.pmf(i,lamda)
    p_recursion = py[i]
    p_normalized = p_recursion/total_sum
    f_writer.writerow([i,p_formula,p_recursion,p_normalized])

'''

from scipy.stats import poisson

lambda_param = 10000
k = 10100  # Example: probability of getting 10100 events

# Calculate the probability mass at point k
pmf_value = poisson.pmf(k, lambda_param)
print(f"P(X = {k}) = {pmf_value}")

# Calculate the cumulative probability P(X <= k)
cdf_value = poisson.cdf(k, lambda_param)
print(f"P(X <= {k}) = {cdf_value}")

# Calculate the survival function P(X > k) = 1 - P(X <= k)
sf_value = poisson.sf(k, lambda_param)
print(f"P(X > {k}) = {sf_value}")
'''