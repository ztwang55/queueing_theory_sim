import random
import math

NUM_ROWS = 7
NUM_COLS = 7
NUM_CELLS = NUM_ROWS * NUM_COLS  # 49 cells
NEIGHBORS = {}  # Adjacency list

K = 10            # Channels per cell
MU = 1.0 / 120.0  # Service rate (1/mean holding time)
DELTA = 1.0 / 60.0 # Handover rate (1/dwell time)
MAX_ARRIVALS = 50000 # Stop simulation after this many new call arrivals [cite: 2653]

def generate_hex_neighbors():
    global NEIGHBORS
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            cell_id = r * NUM_COLS + c
            neighs = []
            if r % 2 == 0: # Even row
                offsets = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]
            else:          # Odd row
                offsets = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
            
            for dr, dc in offsets:
                nr, nc = (r + dr) % NUM_ROWS, (c + dc) % NUM_COLS
                n_id = nr * NUM_COLS + nc
                neighs.append(n_id)
            NEIGHBORS[cell_id] = neighs

def erlang_b(A, k):
    if A == 0: return 0.0
    inv_B = 1.0
    for i in range(1, k + 1):
        inv_B = 1 + (i / A) * inv_B
    return 1.0 / inv_B

def run_efpa(lam_per_cell):
    theta = [lam_per_cell] * NUM_CELLS 
    B = [0.0] * NUM_CELLS
    
    p_h = DELTA / (MU + DELTA) 
    p_ij = p_h * (1.0 / 6.0)   
    
    tolerance = 1e-6
    max_iter = 100
    
    for _ in range(max_iter):
        old_theta = list(theta)
        effective_service_rate = MU + DELTA
        for i in range(NUM_CELLS):
            offered_load = theta[i] / effective_service_rate
            B[i] = erlang_b(offered_load, K)
            
        max_diff = 0.0
        for i in range(NUM_CELLS):
            sum_handovers = 0.0
            for j in NEIGHBORS[i]:
                sum_handovers += (1 - B[j]) * theta[j] * p_ij
            new_theta_i = lam_per_cell + sum_handovers
            diff = abs(new_theta_i - old_theta[i])
            if diff > max_diff:
                max_diff = diff
            theta[i] = new_theta_i
            
        if max_diff < tolerance:
            break
            
    return sum(B) / NUM_CELLS 

def run_simulation(lam_per_cell):
    Q = [0] * NUM_CELLS
    Na = [0] * NUM_CELLS # Arrivals
    Nb = [0] * NUM_CELLS # Blocked Arrivals
    Nh = [0] * NUM_CELLS # Handovers attempts (into cell)
    Nd = [0] * NUM_CELLS # Dropped Handovers
    total_arrivals = 0
    while total_arrivals < MAX_ARRIVALS:
        sum_lambda = lam_per_cell * NUM_CELLS
        sum_Q_mu = sum(Q) * MU
        sum_Q_delta = sum(Q) * DELTA
        total_rate = sum_lambda + sum_Q_mu + sum_Q_delta
        R = random.random()
        p_arr = sum_lambda / total_rate
        p_dep = sum_Q_mu / total_rate
        if R <= p_arr:
            threshold = R * total_rate
            current_sum = 0
            target_cell = -1
            for i in range(NUM_CELLS):
                current_sum += lam_per_cell
                if current_sum >= threshold:
                    target_cell = i
                    break
            if target_cell == -1: target_cell = NUM_CELLS - 1
            Na[target_cell] += 1
            total_arrivals += 1
            if Q[target_cell] < K:
                Q[target_cell] += 1
            else:
                Nb[target_cell] += 1       
        elif R <= p_arr + p_dep:
            threshold = (R - p_arr) * total_rate
            current_sum = 0
            for i in range(NUM_CELLS):
                current_sum += Q[i] * MU
                if current_sum >= threshold:
                    Q[i] -= 1
                    break
        else:
            threshold = (R - p_arr - p_dep) * total_rate
            current_sum = 0
            source_cell = -1
            for i in range(NUM_CELLS):
                current_sum += Q[i] * DELTA
                if current_sum >= threshold:
                    source_cell = i
                    Q[i] -= 1 # Decrement source immediately
                    break      
            if source_cell != -1:
                neighs = NEIGHBORS[source_cell]
                dest_cell = random.choice(neighs)
                Nh[dest_cell] += 1
                if Q[dest_cell] < K:
                    Q[dest_cell] += 1
                else:
                    Nd[dest_cell] += 1
    
    total_Nb = sum(Nb)
    total_Na = sum(Na)
    total_Nd = sum(Nd)
    total_Nh = sum(Nh)
    P_B = total_Nb / total_Na if total_Na > 0 else 0 
    P_D = total_Nd / total_Nh if total_Nh > 0 else 0 
    P_Combined = (total_Nb + total_Nd) / (total_Na + total_Nh)
    return P_B, P_D, P_Combined

if __name__ == "__main__":
    generate_hex_neighbors()
    
    print(f"{'Lambda':<10} | {'Sim P_Block':<12} | {'Sim P_Drop':<12} | {'Sim Combined':<12} | {'EFPA B':<10}")
    print("-" * 65)
    test_lambdas = [0.15, 0.20, 0.25, 0.30] 
    
    for lam in test_lambdas:
        pb_sim, pd_sim, p_comb_sim = run_simulation(lam)
        b_efpa = run_efpa(lam)
        print(f"{lam:<10.2f} | {pb_sim:<12.4f} | {pd_sim:<12.4f} | {p_comb_sim:<12.4f} | {b_efpa:<10.4f}")