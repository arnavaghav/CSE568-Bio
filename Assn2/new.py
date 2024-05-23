import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import entropy

def compute_confidence_interval(n, p_hat, z=1.96):
    se = np.sqrt(p_hat * (1 - p_hat) / n)
    return p_hat - z * se, p_hat + z * se

def calculate_privacy(data, reconstructed_data):
    """
    Calculate the privacy metric based on the maximum a posteriori probability.
    The entropy of the distribution is used as a simplification to measure privacy.
    """
    original_prob = data.value_counts(normalize=True)
    reconstructed_prob = reconstructed_data.value_counts(normalize=True)
    privacy_metric = entropy(original_prob, reconstructed_prob)
    return privacy_metric

def calculate_utility(original_data, reconstructed_data):
    """
    Utility is calculated as the mean squared error between the original and
    reconstructed data distributions.
    """
    original_prob = original_data.value_counts(normalize=True)
    reconstructed_prob = reconstructed_data.value_counts(normalize=True)
    mse = ((original_prob - reconstructed_prob) ** 2).mean()
    return mse

# Load survey response data
data = pd.read_csv('samples.csv')
gt_data = pd.read_csv('gt.csv')  # Ground truth for syphilis

# Part I: Compute histogram and confidence intervals for each disease
diseases = ['chlamydia', 'gonorrhea', 'syphilis', 'herpes', 'hiv']
alpha = len(diseases)  # Number of diseases in the study
P = data.shape[0]  # Total number of participants
disease_counts = data['negative_disease'].value_counts()

# Estimate the prevalence
estimated_prevalence = {disease: P - count * (alpha - 1) for disease, count in disease_counts.items()}
confidence_intervals = {disease: compute_confidence_interval(P, count / P) for disease, count in estimated_prevalence.items()}

# Calculate privacy and utility for syphilis
privacy_value = calculate_privacy(gt_data['disease'], pd.Series(['syphilis']*len(gt_data)))
utility_value = calculate_utility(gt_data['disease'], pd.Series(['syphilis']*len(gt_data)))

print(f"Privacy Value for Syphilis: {privacy_value}, Utility Value for Syphilis: {utility_value}")

# Visualization of disease prevalence with confidence intervals
fig, ax = plt.subplots(figsize=(10, 6))
errors = [(estimated_prevalence[disease] * (ci[1] - ci[0]) / 2) for disease, ci in confidence_intervals.items()]
ax.bar(estimated_prevalence.keys(), estimated_prevalence.values(), yerr=errors, capsize=5)
ax.set_xlabel('Disease')
ax.set_ylabel('Estimated Number of Cases')
ax.set_title('Estimated Disease Prevalence with 95% Confidence Intervals')
plt.xticks(rotation=45)
plt.show()
