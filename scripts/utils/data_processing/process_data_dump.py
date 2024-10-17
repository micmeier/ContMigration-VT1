import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def calc_stats(data):
    stats = data.describe().transpose()
    
    stats['median'] = data.median()
    stats['mean'] = data.mean()
    
    return stats

def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

def plot_hist_with_outliers(data):
    columns = data.columns[1:]
    
    for column in columns:
        plt.figure(figsize=(10, 6))
        plt.hist(data[column].dropna(), bins=15, edgecolor='k', alpha=0.7)
        plt.title(f'Histogram of {column}-Time for a Migration of a Disk Intensive Application with 3452 KB Load')
        plt.xlabel(f'{column} [ms]')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.savefig(f'{column}_plot.pdf', bbox_inches='tight')
        plt.show()
        
def plot_hist_without_outliers(data):
    columns = data.columns[1:]
    
    for column in columns:
        column_data_no_outliers = remove_outliers(data, column)
        plt.figure(figsize=(10, 6))
        plt.hist(column_data_no_outliers[column].dropna(), bins=20, edgecolor='k', alpha=0.7)
        plt.title(f'Histogram of {column}-Time for a Migration of a Disk Intensive Application without outliers')
        plt.xlabel(f'{column} [ms]')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()
        
def plot_scatter_with_outliers(data):
    columns = data.columns[1:]
    
    for column in columns:
        plt.plot(data[column])
        plt.title(f'{column}-Time for Migrations of a Memory Intensive Application with 83.98 MB Load')
        plt.xlabel('Iteration')
        plt.ylabel('Duration [ms]')
        plt.grid(True)
       # plt.savefig(f'{column}_plot.pdf', bbox_inches='tight')

        plt.show()
        
def plot_scatter_without_outliers(data):
    columns = data.columns[1:]
    
    for column in columns:
        columns = remove_outliers(data, column)
        plt.plot(data[column])
        plt.title(f'{column}-Time for Migrations of a Memory Intensive Application without outliers')
        plt.xlabel('Iteration')
        plt.ylabel('Duration [ms]')
        plt.grid(True)
        #plt.savefig(f'{column}_plot.pdf', bbox_inches='tight')
        plt.show()

input_file_path = 'C:/Users/rinik/OneDrive/Desktop/ZHAW//07_HS23/PA/ContMigration/utils/data_extraction/data_dump/mongo-0_migration_times_100k.csv'
output_file_path = 'C:/Users/rinik/OneDrive/Desktop/ZHAW//07_HS23/PA/ContMigration/utils/data_processing/disk/mongo100k_migration-times.csv'

data_raw = pd.read_csv(input_file_path, delimiter=',')

# some stats with outliers
data_raw_stats = calc_stats(data_raw)

plot_hist_with_outliers(data_raw)
#plot_hist_without_outliers(data_raw)
#plot_scatter_with_outliers(data_raw)
#plot_scatter_without_outliers(data_raw)

data_raw_stats.to_csv(output_file_path)


