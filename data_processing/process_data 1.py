import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

def read_data(file_path):
    with open(file_path, 'r') as file:
        data = [int(line.strip()) for line in file]
    return data

def filter_data(data):
    # remove "corrupt" data (over 30s means timeout has not been detected by K8s)
    data = [x for x in data if x < 30000]
    return data

def create_scatter_plot(data, title):
    # Calculate iterations and basic statistics
    iterations = len(data)
    average_ms = np.mean(data)
    median_ms = np.median(data)
    std_dev_ms = np.std(data)
    min_duration = np.min(data)
    max_duration = np.max(data)

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.title(title)
    plt.plot(data, marker='o', label='Duration')
    plt.xlabel('Iteration')
    plt.ylabel('Duration (ms)')
    plt.axhline(y=average_ms, color='r', linestyle='--', label=f'Average ({average_ms:.2f} ms)')
    plt.axhline(y=median_ms, color='g', linestyle='--', label=f'Median ({median_ms} ms)')
    plt.axhline(y=std_dev_ms, color='b', linestyle='--', label=f'Standard Deviation ({std_dev_ms:.2f} ms)')
    plt.axhline(y=min_duration, color='y', linestyle='--', label=f'Minimum ({min_duration} ms)')
    plt.axhline(y=max_duration, color='purple', linestyle='--', label=f'Maximum ({max_duration} ms)')
    plt.fill_between(range(iterations), average_ms - std_dev_ms, average_ms + std_dev_ms, color='gray', alpha=0.3, label='SD Range')

    # Move the legend to the top of the plot
    plt.legend(bbox_to_anchor=(0.5, 1.15), loc='lower center', ncol=3)

    plt.grid(True)
    plt.tight_layout()
    
    savefile = 'C:/Users/rinik/OneDrive/Desktop/ZHAW/07_HS23/PA/ContMigration/data_processing/plots/scatterplot.pdf'
    print(savefile)

    plt.savefig(savefile)
    
    plt.show()
    
def create_hist_plot(data, title):  
    mu, std = norm.fit(data)
    
    bins = np.arange(0, max(data) + 5000, 5000)
    plt.hist(data, edgecolor="black", bins=bins)
    
    plt.title(title)
    plt.xlabel("Time of Migration [ms]")
    plt.ylabel("Amount of Migrations")
    plt.grid(axis="y")
    
    savefile = 'C:/Users/rinik/OneDrive/Desktop/ZHAW/07_HS23/PA/ContMigration/data_processing/plots/histogram.pdf'
    print(savefile)
    plt.savefig(savefile)
    plt.show()
    


file_dir_mem = "C:/Users/rinik/OneDrive/Desktop/ZHAW/07_HS23/PA/ContMigration/mem_intensive/data/"
file_dir_drw = "C:/Users/rinik/OneDrive/Desktop/ZHAW/07_HS23/PA/ContMigration/disk_rw_intensive/data/"

path_m_mem_kf = file_dir_mem + "migration_duration_kill_first.txt"
path_d_mem_kf = file_dir_mem + "pod_downtime_kill_first.txt"

path_m_mem_rf = file_dir_mem + "migration_duration_replicate_first.txt"
path_d_mem_rf = file_dir_mem + "pod_downtime_kill_first.txt"

path_m_drw_kf = file_dir_drw + "migration_duration_mongo_kill_first.txt"
path_d_drw_kf = file_dir_drw + "pod_downtime_mongo_kill_first.txt"

path_m_mem_kf_local = file_dir_mem + "migration_duration_kill_first_local.txt"
path_d_mem_kf_local = file_dir_mem + "pod_downtime_kill_first_local.txt"

#data_m_mem_kf = read_data(path_m_mem_kf)
#data_d_mem_kf = read_data(path_d_mem_kf)

data_m_mem_kf_local = read_data(path_m_mem_kf_local)
data_d_mem_kf_local = read_data(path_d_mem_kf_local)

#data_m_mem_rf = read_data(path_m_mem_rf)
#data_d_mem_rf = read_data(path_d_mem_rf)

#data_m_drw_kf = read_data(path_m_drw_kf)
#data_d_drw_kf = read_data(path_d_drw_kf)

data = data_m_mem_kf_local
title = "Kill-First Pod Downtime Without Running Application"

create_scatter_plot(filter_data(data), title)
data.sort()
#create_scatter_plot(filter_data(data), title)
#create_hist_plot(filter_data(data), title)
