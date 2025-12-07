import os
import math
import csv

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'poisson_distribution.csv')

#set parameter: \lambda
lamda = 11

#set variable range: i
i_max = 100

#set initial value: P(X=0)=exp(-lambda)*1/1 for formula, P(Y=0)=1 for recursion
px0=math.exp(-1*lamda)
py0 = 1

#create csv file
f = open(file_path, 'w', encoding='utf-8', newline="")
f_writer = csv.writer(f)
f_writer.writerow(["lambda",lamda])
f_writer.writerow(["i","Poisson distribution formula","Values based on recursion","Normalised values"])

#for normalization, calculate the sum of former i P(Y=i)
def cal_poisson(i):
    if i==0:
        return py0
    return lamda / i * cal_poisson(i - 1)

def cal_poisson_sum(i):
    if i==0:
        return py0
    return cal_poisson(i) + cal_poisson_sum(i-1)

sum = cal_poisson_sum(i_max)

p_recursion = py0
f_writer.writerow([0,px0,py0,py0/sum])

for i in range(1,i_max):
    p_formula = px0 * math.pow(lamda,i) / math.factorial(i)
    p_recursion = p_recursion * lamda / i
    p_normalized = p_recursion/sum
    f_writer.writerow([i,p_formula,p_recursion,p_normalized])
