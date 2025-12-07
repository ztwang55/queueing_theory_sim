import numpy as np
import matplotlib.pyplot as plt
# 1. Set parameters
lambda_param = 1  # This is the rate parameter λ
num_samples = 100000
# 2. Generate Uniform(0,1) deviates
u = np.random.uniform(0, 1, num_samples)
# 3. Apply the inverse transform to generate Exponential(λ) deviates
# This is the key line implementing your formula: x = -ln(u) / λ
x = -np.log(u) / lambda_param
# 4. Plot the histogram
plt.figure(figsize=(10, 6))
# 'density=True' normalizes the histogram so the area sums to 1,
# allowing us to overlay the density for comparison.
count, bins, ignored = plt.hist(x, bins=100, density=True, alpha=0.7, color='lightblue', edgecolor='black', label='Generated Data (Histogram)')
# 5. Plot the theoretical Exponential(λ) density for comparison
x_theoretical = np.linspace(0, np.max(x), 1000) # Create points on the x-axis
y_theoretical = lambda_param * np.exp(-lambda_param * x_theoretical) # Calculate f(x) = λe^{-λx}
plt.plot(x_theoretical, y_theoretical, 'r-', linewidth=2, label='Theoretical density')
# 6. Add labels and title
plt.title('Histogram of Generated Exponential(λ=1) Deviates')
plt.xlabel('x (Time to Event)')
plt.ylabel('Density')
plt.legend()
plt.xlim(0, 6) # Limit x-axis to see the important part. Some very large values are possible but rare.
plt.grid(True, alpha=0.3)
plt.show()