import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_data(filename):
    """ Load data from CSV file. """
    return pd.read_csv(filename)

def bin_data(data, bins=5):
    """ Bin latitude and longitude data. """
    labels = range(bins)
    data['lat_bin'] = pd.cut(data['negative_lat'], bins=bins, labels=labels)
    data['lon_bin'] = pd.cut(data['negative_lon'], bins=bins, labels=labels)
    return data

def calculate_prevalence(data, diseases):
    """ Calculate prevalence for each disease based on negative survey method. """
    # Initialize a dictionary to hold prevalence data
    prevalence = {disease: np.zeros((5, 5)) for disease in diseases}

    total_count = data.groupby(['lat_bin', 'lon_bin']).size().unstack(fill_value=0)
    
    for disease in diseases:
        disease_data = data[data['negative_disease'] == disease]
        count = disease_data.groupby(['lat_bin', 'lon_bin']).size().unstack(fill_value=0)
        prevalence[disease] = (total_count - count).div(total_count).fillna(0).to_numpy()

    return prevalence

def plot_heatmaps(prevalence):
    """ Plot heatmaps for each disease. """
    for disease, data in prevalence.items():
        plt.figure(figsize=(10, 8))
        sns.heatmap(data, annot=True, cmap='viridis', fmt=".2f", linewidths=.5)
        plt.title(f'Prevalence of {disease}')
        plt.xlabel('Longitude Bin')
        plt.ylabel('Latitude Bin')
        plt.show()
        plt.savefig(f'{disease}_heatmap.png')

def main():
    data = load_data('samples.csv')
    diseases = ['chlamydia', 'gonorrhea', 'syphilis', 'herpes', 'hiv']
    binned_data = bin_data(data)
    prevalence = calculate_prevalence(binned_data, diseases)
    plot_heatmaps(prevalence)

if __name__ == "__main__":
    main()
