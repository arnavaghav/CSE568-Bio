import csv
import math
import numpy as np
import matplotlib.pyplot as plt

# Part I: One-dimensional reconstruction
def reconstruct_1d(responses, num_diseases):
    counts = [0] * num_diseases
    for resp in responses:
        if len(resp) > 0:  # Check if the row is not empty
            disease = resp[0]
            if disease >= 0 and disease < num_diseases:  # Check if the disease value is valid
                counts[disease] += num_diseases - 1
    total_responses = len(responses)
    estimates = [count / (num_diseases - 1) - total_responses for count in counts]
    return estimates

# Function to read data from CSV file
def read_csv(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            if any(x.isdigit() for x in row):  # Check if the row has at least one numeric value
                data.append([int(x) if x.isdigit() else -1 for x in row])
    return data

def read_ground_truth(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        header = next(reader, None)  # Skip header row, if present
        if header is not None:
            ground_truth = [int(x) for row in reader for x in row if x.isdigit()]
        else:
            ground_truth = [int(x) for x in next(reader, []) if x.isdigit()]
    return ground_truth

# Function to compute privacy and utility metrics
def compute_metrics(estimates, ground_truth):
    if len(estimates) != len(ground_truth):
        print("Error: Estimates and ground truth have different lengths.")
        return None, None

    privacy = 0
    utility = 0
    num_categories = len(estimates)
    for i in range(num_categories):
        privacy += abs(estimates[i] - ground_truth[i]) / (num_categories - 1)
        utility += abs(estimates[i] - ground_truth[i])
    privacy /= num_categories
    utility = 1 - utility / (2 * sum(ground_truth))
    return privacy, utility

# Part I
num_diseases = 5
samples = read_csv('samples.csv')
estimates = reconstruct_1d(samples, num_diseases)
print(f"Length of estimates: {len(estimates)}")


# Histogram for Part I
diseases = ['chlamydia', 'gonorrhea', 'syphilis', 'hiv', 'herpes']
plt.bar(diseases, estimates)
plt.xlabel('Disease')
plt.ylabel('Estimated Prevalence')
plt.title('Estimated Prevalence of Diseases')
plt.show()

# Experiment with different sample sizes
sample_sizes = [100, 500, 1000, 5000, 10000]
times = []
confidences = []
for size in sample_sizes:
    samples = read_csv('samples.csv')[:size]
    estimates = reconstruct_1d(samples, num_diseases)
    times.append(len(samples))
    confidences.append(np.std(estimates) / math.sqrt(size))

plt.plot(times, confidences)
plt.xlabel('Number of Samples')
plt.ylabel('Standard Error')
plt.title('Standard Error vs. Number of Samples')
plt.show()

# Compute privacy and utility for syphilis

# ground_truth = [int(x) for x in open('gt.csv', 'r').readline().split(',')[1:]]
# ground_truth = read_ground_truth('gt.csv')
# Compute privacy and utility for syphilis
with open('gt.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip header row
    ground_truth = [int(x) for x in next(reader) if x.isdigit()]

print(f"Length of ground truth: {len(ground_truth)}")

if len(estimates) == len(ground_truth):
    privacy, utility = compute_metrics(estimates, ground_truth)
    print(f"Privacy for syphilis: {privacy}")
    print(f"Utility for syphilis: {utility}")
else:
    print("Error: Estimates and ground truth have different lengths.")

print(f"Length of ground truth: {len(ground_truth)}")
privacy, utility = compute_metrics(estimates, ground_truth)
print(f"Privacy for syphilis: {privacy}")
print(f"Utility for syphilis: {utility}")

# Part II: Two-dimensional reconstruction
def reconstruct_2d(responses, num_cities, num_diseases):
    counts = [[0] * num_cities for _ in range(num_diseases)]
    for resp in responses:
        disease, city = resp[:2]
        disease = int(disease)
        city = int(city)
        counts[disease][city - 1] += num_cities - 1
        for i in range(num_cities):
            if i != city - 1:
                counts[disease][i] += 1
    total_responses = len(responses)
    estimates = [[0] * num_cities for _ in range(num_diseases)]
    for i in range(num_diseases):
        for j in range(num_cities):
            estimates[i][j] = counts[i][j] / (num_cities - 1) - total_responses
    return estimates

# Part II
num_cities = 5
num_diseases = 2  # Only considering herpes
samples = read_csv('samples.csv')
estimates = reconstruct_2d(samples, num_cities, num_diseases)

# Histogram for herpes prevalence in each city
cities = [f'City {i+1}' for i in range(num_cities)]
plt.bar(cities, estimates[1])
plt.xlabel('City')
plt.ylabel('Estimated Prevalence of Herpes')
plt.title('Estimated Prevalence of Herpes in Different Cities')
plt.show()