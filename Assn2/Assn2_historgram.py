import numpy as np
import matplotlib.pyplot as plt

# Count the number of responses for each disease
response_counts = data['negative_disease'].value_counts()

# Total number of participants (P) and number of diseases (alpha)
P = len(data)
alpha = 4  # The diseases are chlamydia, gonorrhea, syphilis, herpes

# Calculate the estimated occurrence of each disease
estimated_occurrences = {disease: P - count * (alpha - 1) for disease, count in response_counts.items()}

# Convert to a more suitable structure for plotting
diseases = list(estimated_occurrences.keys())
estimates = list(estimated_occurrences.values())

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(diseases, estimates, color='skyblue')
plt.title('Estimated Occurrence of Each Disease')
plt.xlabel('Disease')
plt.ylabel('Estimated Number of Occurrences')
plt.xticks(rotation=45)
plt.grid(axis='y')

plt.show()
