import numpy as np
from scipy.special import factorial

class GGkKQueue:
    def __init__(self, k, arrival_type, service_type, arrival_params, service_params):
        self.k = k
        self.arrival_type = arrival_type
        self.service_type = service_type
        self.arrival_params = arrival_params
        self.service_params = service_params
    
    def generate_interarrival(self):
        if self.arrival_type == "exponential":
            return np.random.exponential(1/self.arrival_params[0])
        elif self.arrival_type == "uniform":
            return np.random.uniform(self.arrival_params[0], self.arrival_params[1])
    
    def generate_service(self):
        if self.service_type == "exponential":
            return np.random.exponential(1/self.service_params[0])
        elif self.service_type == "uniform":
            return np.random.uniform(self.service_params[0], self.service_params[1])
    
    def simulate(self, num_customers=50000):
        blocked = 0
        served = 0
        current_time = 0
        servers = np.zeros(self.k)  
        
        for i in range(num_customers):
            interarrival = self.generate_interarrival()
            current_time += interarrival
            service_time = self.generate_service()
            
            available = None
            for j in range(self.k):
                if servers[j] <= current_time:
                    available = j
                    break
            
            if available is not None:
                servers[available] = current_time + service_time
                served += 1
            else:
                blocked += 1
        
        blocking_prob = blocked / num_customers
        offered_traffic = num_customers * np.mean([self.generate_service() for _ in range(1000)])
        carried_traffic = served * np.mean([self.generate_service() for _ in range(1000)])
        
        return blocking_prob, offered_traffic, carried_traffic

def erlang_b(A, k):
    """Erlang B formula"""
    numerator = (A ** k) / factorial(k)
    denominator = sum([(A ** i) / factorial(i) for i in range(k + 1)])
    return numerator / denominator

# parameters
k_values = [1, 2, 5, 10]
offered_traffics = [0.5, 1.0, 2.0, 5.0, 8.0]  #  A

print("G/G/k/k Blocking Probability Analysis")
print("=" * 60)
print("A = Offered Traffic (erlangs)")
print("Pb = Blocking Probability")
print("Carried Traffic = A × (1 - Pb)")
print("=" * 60)

for k in k_values:
    print(f"\nServers: k = {k}")
    print("A\tM/M/k/k Pb(Sim)\tM/M/k/k Pb(Theory)\tU/U/k/k Pb(Sim)")
    print("-" * 70)
    
    for A in offered_traffics:
        if A > k * 3:  
            continue
            
        # M/M/k/k 
        lambda_arrival = A  #  offered traffic = A
        mu_service = 1.0    
        
        mmkk = GGkKQueue(k, "exponential", "exponential", [lambda_arrival], [mu_service])
        mmkk_pb, mmkk_offered, mmkk_carried = mmkk.simulate(30000)
        theory_pb = erlang_b(A, k)
        
        # U/U/k/k 
        mean_interarrival = 1.0 / lambda_arrival
        uukk = GGkKQueue(k, "uniform", "uniform", 
                        [0.5*mean_interarrival, 1.5*mean_interarrival], 
                        [0.5, 1.5])  # mean=1.0
        uukk_pb, uukk_offered, uukk_carried = uukk.simulate(30000)
        
        print(f"{A:.1f}\t{mmkk_pb:.4f}\t\t{theory_pb:.4f}\t\t\t{uukk_pb:.4f}")
    
    # Carried Traffic = Offered Traffic × (1 - Pb)
    print(f"\nVerification for k={k}:")
    test_A = 2.0  
    if test_A <= k * 3:
        lambda_test = test_A
        test_queue = GGkKQueue(k, "exponential", "exponential", [lambda_test], [1.0])
        pb, offered, carried = test_queue.simulate(10000)
        calculated_carried = offered * (1 - pb)
        print(f"Offered Traffic: {offered:.3f}")
        print(f"Blocking Prob: {pb:.4f}")
        print(f"Carried Traffic (sim): {carried:.3f}")
        print(f"Carried Traffic (calc): {calculated_carried:.3f}")
        print(f"Difference: {abs(carried - calculated_carried):.3f}")