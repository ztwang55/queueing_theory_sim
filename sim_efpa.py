import math

def erlang_b(A, k):
    if A == 0: return 0.0
    inv_B = 1.0
    for i in range(1, k + 1):
        inv_B = 1 + (i / A) * inv_B
    return 1.0 / inv_B

k = 20
Traffic_Direct_23 = 12.0
Traffic_Direct_34 = 11.0
Traffic_Route_234 = 9.0

B_23 = 0.0
B_34 = 0.0

print(f"{'Iter':<5} | {'Load a_23':<10} | {'Load a_34':<10} | {'B_23':<10} | {'B_34':<10}")
print("-" * 55)

for i in range(10):
    a_23 = Traffic_Direct_23 + Traffic_Route_234 * (1 - B_34)
    a_34 = Traffic_Direct_34 + Traffic_Route_234 * (1 - B_23)
    B_23_new = erlang_b(a_23, k)
    B_34_new = erlang_b(a_34, k)
    print(f"{i:<5} | {a_23:<10.4f} | {a_34:<10.4f} | {B_23_new:<10.6f} | {B_34_new:<10.6f}")
    B_23 = B_23_new
    B_34 = B_34_new

print("-" * 55)
Prob_Block_Route_23 = B_23
Prob_Block_Route_34 = B_34
Prob_Block_Route_234 = 1 - (1 - B_23) * (1 - B_34)

print(f"\nFinal Results:")
print(f"Blocking Probability Route 2->3:       {Prob_Block_Route_23:.6f}")
print(f"Blocking Probability Route 3->4:       {Prob_Block_Route_34:.6f}")
print(f"Blocking Probability Route 2->3->4:    {Prob_Block_Route_234:.6f}")