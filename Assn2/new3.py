import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from scipy.stats import entropy

def compute_confidence_interval(n, p_hat, z=1.96):
    """Compute 95% confidence interval for binomial distribution estimate."""
    se = np.sqrt(p_hat * (1 - p_hat) / n)
    return p_hat - z * se, p_hat + z * se

def load_data():
    data = pd.read_csv('samples.csv')
    return data

def calculate_histogram(data):
    diseases = ['chlamydia', 'gonorrhea', 'syphilis', 'herpes', 'hiv']
    counts = data['negative_disease'].value_counts()
    P = len(data)
    alpha = len(diseases)
    prevalence = {disease: P - counts.get(disease, 0) * (alpha - 1) for disease in diseases}
    ci = {disease: compute_confidence_interval(P, counts.get(disease, 0) / P) for disease in diseases}
    return prevalence, ci

def plot_histogram(prevalence, ci):
    fig, ax = plt.subplots()
    diseases = list(prevalence.keys())
    counts = list(prevalence.values())
    errors = [(ci[disease][1] - ci[disease][0]) / 2 for disease in diseases]
    ax.bar(diseases, counts, yerr=errors, color='blue', alpha=0.7)
    ax.set_ylabel('Estimated Prevalence')
    ax.set_title('Disease Prevalence with Confidence Intervals')
    plt.xticks(rotation=45)
    plt.savefig('Disease_Prevalence_Histogram.png')
    plt.show()

def sample_experiment(data, samples):
    results = []
    for sample_size in samples:
        start = time.time()
        sampled_data = data.sample(n=sample_size, replace=True)
        prevalence, ci = calculate_histogram(sampled_data)
        end = time.time()
        results.append((sample_size, end - start, ci))
    return results

def plot_city_histogram(data):
    city_counts = data[data['negative_disease'] == 'herpes']['negative_city'].value_counts()
    plt.figure(figsize=(10, 6))
    plt.bar(city_counts.index.map(str), city_counts.values, color='green')
    plt.xlabel('City Code')
    plt.ylabel('Number of Non-Herpes Reports')
    plt.title('Herpes Prevalence in Cities')
    plt.xticks(rotation=45)
    plt.savefig('Herpes_Prevalence_Cities.png')
    plt.show()

def main():
    data = load_data()
    prevalence, ci = calculate_histogram(data)
    plot_histogram(prevalence, ci)
    
    experiment_results = sample_experiment(data, [100, 500, 1000, 5000, 10000])
    for result in experiment_results:
        print(f'Sample size: {result[0]}, Time: {result[1]:.4f} seconds')
    
    plot_city_histogram(data)

if __name__ == "__main__":
    main()
