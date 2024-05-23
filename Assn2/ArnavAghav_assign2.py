import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.stats import binom

# Function to compute confidence intervals for a binomial distribution
def compute_confidence_interval(n, p_hat, z=1.96):
    se = np.sqrt(p_hat * (1 - p_hat) / n)
    return p_hat - z * se, p_hat + z * se

# Load survey response data
data = pd.read_csv('samples.csv')

# Part I: Compute histogram and confidence intervals for each disease
diseases = ['chlamydia', 'gonorrhea', 'syphilis', 'herpes', 'hiv']
alpha = len(diseases)  # Number of diseases in the study
P = data.shape[0]  # Total number of participants
disease_counts = data['negative_disease'].value_counts()

# Estimate the prevalence
estimated_prevalence = {disease: P - count * (alpha - 1) for disease, count in disease_counts.items()}
confidence_intervals = {disease: compute_confidence_interval(P, count / P) for disease, count in estimated_prevalence.items()}

# Plotting the histogram with confidence intervals
fig, ax = plt.subplots(figsize=(10, 6))
errors = [(estimated_prevalence[disease] * (ci[1] - ci[0]) / 2) for disease, ci in confidence_intervals.items()]
ax.bar(estimated_prevalence.keys(), estimated_prevalence.values(), yerr=errors, capsize=5)
ax.set_xlabel('Disease')
ax.set_ylabel('Estimated Number of Cases')
ax.set_title('Estimated Disease Prevalence with 95% Confidence Intervals')
plt.xticks(rotation=45)
plt.show()

# Part II: Compute privacy and utility values for syphilis
# Assuming functions for privacy and utility calculations are defined
# Placeholder functions (implement based on paper specifics)
def calculate_privacy(data):
    return np.random.random()

def calculate_utility(data):
    return np.random.random()

gt_data = pd.read_csv('gt.csv')  # Load ground truth data for syphilis
privacy_value = calculate_privacy(gt_data)
utility_value = calculate_utility(gt_data)

print(f"Privacy Value: {privacy_value}, Utility Value: {utility_value}")

# Part III: Sample size variation experiment
sample_sizes = [100, 500, 1000, 5000, 10000]
results = []

for size in sample_sizes:
    start_time = time.time()
    sampled_data = data['negative_disease'].sample(n=size, replace=True)
    count_data = sampled_data.value_counts(normalize=True)
    ci_bounds = {disease: compute_confidence_interval(size, count_data.get(disease, 0)) for disease in diseases}
    end_time = time.time()
    results.append({
        'Sample Size': size,
        'Computation Time (s)': end_time - start_time,
        'Confidence Intervals': ci_bounds
    })

# Output results for different sample sizes
results_df = pd.DataFrame(results)
print(results_df)
