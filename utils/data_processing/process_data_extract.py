import pandas as pd
import matplotlib.pyplot as plt

def remove_outliers(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    data_no_outliers = data[~((data < lower_bound) | (data > upper_bound)).any(axis=1)]
    return data_no_outliers

def calc_stats(data):
    data_no_outliers = remove_outliers(data)
    
    stats = data_no_outliers.describe().transpose()
    stats['median'] = data_no_outliers.median()
    stats['mean'] = data_no_outliers.mean()
    
    return stats

def plot_hist_with_outliers(data):
    columns = data.columns
    
    for column in columns:
        plt.figure(figsize=(10, 6))
        plt.hist(data[column].dropna(), bins=10, edgecolor='k', alpha=0.7)
        plt.title(f'Histogram of {column} for the checkpointing process of a CPU Intensive Application')
        plt.xlabel(f'{column} [ms]')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.savefig(f'{column}_plot.pdf', bbox_inches='tight')
        plt.show()
        
def plot_scatter_without_outliers(data):
    columns = data.columns
    
    for column in columns:
        plt.plot(data[column])
        plt.title(f'{column}-Time for checkpointing a Memory Intensive Application')
        plt.xlabel('Iteration')
        plt.ylabel('Duration [ms]')
        plt.grid(True)
        #plt.savefig(f'{column}_plot.pdf', bbox_inches='tight')

        plt.show()


file_path = 'C:/Users/rinik/OneDrive/Desktop/ZHAW/07_HS23/PA/ContMigration/utils/data_extraction/combined_data/cpu-0-combined-data.csv'  
output_file_path = 'C:/Users/rinik/OneDrive/Desktop/ZHAW//07_HS23/PA/ContMigration/utils/data_processing/disk/mongo10k_checkpointing-times.csv'

data = pd.read_csv(file_path)
data = data.drop(data.columns[:3], axis=1)
#data['Freezing time'] = (data['Freezing time'].astype(float) / 1000.0)

for column in data.columns:
    data[column] = data[column].astype(float)

data_cleaned = remove_outliers(data)

stats = calc_stats(data_cleaned)
plot_hist_with_outliers(data_cleaned)
#plot_scatter_without_outliers(data_cleaned)

#stats.to_csv(output_file_path)