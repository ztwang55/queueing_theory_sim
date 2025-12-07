import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class PP1Queue:
    def __init__(self, alpha_arrival, beta_arrival, alpha_service, beta_service):
        self.alpha_arrival = alpha_arrival
        self.beta_arrival = beta_arrival  
        self.alpha_service = alpha_service
        self.beta_service = beta_service
    
    def pareto_rv(self, alpha, beta):
        return (np.random.pareto(alpha) + 1) * beta
    
    def simulate(self, num_customers=10000, warmup=1000):
        delays = []
        
        queue_records = []  # (time, queue_length)
        current_queue = 0
        current_time = 0
        departure_time = 0
        
        for i in range(num_customers + warmup):
            interarrival = self.pareto_rv(self.alpha_arrival, self.beta_arrival)
            service_time = self.pareto_rv(self.alpha_service, self.beta_service)
            
            queue_records.append((current_time, current_queue))
            
            current_time += interarrival
            
            if current_time >= departure_time:
                delay = 0
                departure_time = current_time + service_time
                current_queue = 1
            else:
                delay = departure_time - current_time
                departure_time += service_time
                current_queue += 1
            
            queue_records.append((current_time, current_queue))
            
            if i >= warmup:
                delays.append(delay)
            
            if current_time >= departure_time:
                current_queue = max(0, current_queue - 1)
                queue_records.append((current_time, current_queue))
        
        queue_records.append((current_time, current_queue))
        
        return np.array(delays), queue_records
    
    def compute_queue_stats(self, queue_records):
        total_time = queue_records[-1][0]
        time_in_state = {}
        
        for i in range(len(queue_records) - 1):
            t_start, q_start = queue_records[i]
            t_end, q_end = queue_records[i + 1]
            duration = t_end - t_start
            
            time_in_state[q_start] = time_in_state.get(q_start, 0) + duration
        
        queue_dist = {q: t/total_time for q, t in time_in_state.items()}
        mean_queue = sum(q * p for q, p in queue_dist.items())
        
        return mean_queue, queue_dist

def run_simulation():
    queue = PP1Queue(alpha_arrival=2.0, beta_arrival=1.0, 
                     alpha_service=2.0, beta_service=0.8)
    
    delays, queue_records = queue.simulate(10000)
    mean_delay = np.mean(delays)
    mean_queue, queue_dist = queue.compute_queue_stats(queue_records)
    
    print(f"Mean delay: {mean_delay:.3f}")
    print(f"Mean queue size: {mean_queue:.3f}")
    
    # 置信区间计算（多轮运行）
    # ... 

if __name__ == "__main__":
    print("P/P/1 Queue Simulation")
    results = run_simulation()