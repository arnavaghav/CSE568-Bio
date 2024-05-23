import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_data(filename):
    """ Load data from CSV file. """
    return pd.read_csv(filename)

def calculate_prevalence(data):
    """ Calculate the non-report rate of herpes in each city. """
    cities = data['negative_city'].unique()
    prevalence = {}

    for city in cities:
        total_responses = len(data[data['negative_city'] == city])
        non_reports = len(data[(data['negative_city'] == city) & (data['negative_disease'] == 'herpes')])
        prevalence[city] = non_reports / total_responses if total_responses > 0 else 0

    return prevalence

def create_heatmap(prevalence):
    """ Create a heatmap from the prevalence data. """
    # Convert the dictionary to a DataFrame
    prevalence_df = pd.DataFrame(list(prevalence.items()), columns=['City', 'Prevalence'])
    prevalence_df.set_index('City', inplace=True)
    prevalence_matrix = prevalence_df.pivot_table(index='City', values='Prevalence')

    # Create the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(prevalence_matrix, annot=True, cmap='viridis', fmt=".2f", linewidths=.5)
    plt.title('Herpes Prevalence in Cities')
    plt.ylabel('City')
    plt.xlabel('Prevalence Rate')
    plt.show()
    plt.savefig('herpes_prevalence_heatmap.png')
    
def main():
    data = load_data('samples.csv')
    prevalence = calculate_prevalence(data)
    create_heatmap(prevalence)

if __name__ == "__main__":
    main()