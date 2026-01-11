import matplotlib.pyplot as plt
import numpy as np
import statistics
import random
import math
import pandas as pd
from scipy import stats

trials = 100000
n = 50

df = pd.read_csv('./data.csv')
rolls = df['Roll'].values
observed_counts = np.bincount(rolls, minlength=21)[1:]  # Exclude index 0

# Expected counts for each value (1-20)
n_total = len(rolls)
expected_freq = n_total / 20
expected_counts = np.full(20, expected_freq)

# Perform chi-squared goodness of fit test
real_chi_squared_stat, _ = stats.chisquare(observed_counts, expected_counts)

def sim(i):
    print(f'{i}/{trials}', end='\r')
    simulated_rolls = np.random.randint(1, 21, size=n_total)
    observed_counts = np.bincount(simulated_rolls, minlength=21)[1:]
    expected_counts = np.full(20, n_total / 20)
    chi_squared_stat, _ = stats.chisquare(observed_counts, expected_counts)
    
    return chi_squared_stat

data = [ sim(i) for i in range(trials) ]
monte_carlo_p_value = sum(1 for x in data if x >= real_chi_squared_stat) / trials

print("p-value: ", monte_carlo_p_value)

plt.hist(data, bins=20, density=True)
# plt.hist(list(range(len(data))), weights=data, bins=n, density=True)
# plt.plot(sorted(data))
# plt.scatter(data, range(len(data)))

plt.axvline(real_chi_squared_stat, color='red', linestyle='--', linewidth=2, 
            label=f'Observed χ² = {real_chi_squared_stat:.2f}\np-value = {monte_carlo_p_value:.4f}')

plt.show()

