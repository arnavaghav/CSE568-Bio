import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import entropy

def compute_confidence_interval(n, p_hat, z=1.96):
    """Compute 95% confidence interval for binomial distribution estimate."""
    se = np.sqrt(p_hat * (1 - p_hat) / n)
    return p_hat - z * se, p_hat + z * se

def calculate_privacy(data, reconstructed_data):
    """Calculate privacy based on the Shannon entropy difference."""
    original_prob = data.value_counts(normalize=True)
    reconstructed_prob = reconstructed_data.value_counts(normalize=True)
    return entropy(original_prob, reconstructed_prob)

def calculate_utility(original_data, reconstructed_data):
    """Calculate utility as the mean squared error between the original and reconstructed distributions."""
    original_prob = original_data.value_counts(normalize=True)
    reconstructed_prob = reconstructed_data.value_counts(normalize=True)
    return ((original_prob - reconstructed_prob) ** 2).mean()


# Load survey response data
data = pd.read_csv('samples.csv')
gt_data = pd.read_csv('gt.csv')  # Ground truth for syphilis

diseases = ['chlamydia', 'gonorrhea', 'syphilis', 'herpes', 'hiv']
alpha = len(diseases)  # Number of diseases in the study
P = data.shape[0]  # Total number of participants
disease_counts = data['negative_disease'].value_counts()


# Ensure each disease has an entry in disease_counts
disease_counts = data['negative_disease'].value_counts()
full_disease_counts = {disease: disease_counts.get(disease, 0) for disease in diseases}

# Number of diseases and participants
diseases = ['chlamydia', 'gonorrhea', 'syphilis', 'herpes', 'hiv']
P = data.shape[0]  # Total number of participants

# Recalculate prevalence and confidence intervals
estimated_prevalence = {disease: P - full_disease_counts.get(disease, 0) * (len(diseases) - 1) for disease in diseases}
confidence_intervals = {disease: compute_confidence_interval(P, full_disease_counts.get(disease, 0) / P) for disease in diseases}

# Generate errors list directly corresponding to the disease order
errors = [(confidence_intervals[disease][1] - confidence_intervals[disease][0]) / 2 for disease in diseases]

# Visualization of disease prevalence with confidence intervals
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(estimated_prevalence.keys(), estimated_prevalence.values(), yerr=errors, capsize=5)
ax.set_xlabel('Disease')
ax.set_ylabel('Estimated Number of Cases')
ax.set_title('Estimated Disease Prevalence with 95% Confidence Intervals')
plt.xticks(rotation=45)
plt.show()
plt.savefig(f'disease_prevalance.png')