import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
plt.style.use('seaborn-deep')


def read_data(file_path):
    with open(file_path, 'r') as file:
        data = [int(line.strip()) for line in file]
    return data

def filter_data(data):
    # remove "corrupt" data (over 30s means timeout has not been detected by K8s)
    data = [x for x in data if x < 28000]
    return data

def create_scatter_plot(data_migr, data_pod, title):
    # Calculate iterations and basic statistics
    iterations = len(data_migr)
    average_duration = np.mean(data_migr)
    average_pod = np.mean(data_pod)
    #median_ms = np.median(data)
    #std_dev_ms = np.std(data)
    
    x = np.linspace(0, 30000, 30000)
    
    min_duration = np.min(data_migr)
    min_pod = np.min(data_pod)
    
    max_duration = np.max(data_migr)
    max_pod = np.max(data_pod)
    

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.title(title)
    
    plt.plot(data_migr, marker='o', label='Total Duration of Migration')
    plt.plot(data_pod, marker='o', label='Pod Downtime')
    
    plt.xlabel('Iteration')
    plt.ylabel('Duration (ms)')
    
    plt.text(x[np.argmax(data_migr)], max_duration, f'Max Migration Time: {max_duration}ms', ha='left', va='bottom', color='black')
    plt.axhline(y=max_duration, color='black', linestyle='--')
    
    plt.text(x[np.argmax(data_migr)], min_duration, f'Min Migration Time: {min_duration}ms', ha='left', va='bottom', color='black')
    plt.axhline(y=min_duration, color='black', linestyle='--')
    
    #plt.text(x[np.argmax(data_pod)], min_pod, f'Min Pod Downtime: {min_pod}ms', ha='left', va='bottom', color='black')
    #plt.axhline(y=min_pod, color='black', linestyle='--')
    
    #plt.text(x[np.argmax(data_pod)], max_pod, f'Max Pod Downtime: {max_pod}ms', ha='left', va='bottom', color='black')
    #plt.axhline(y=max_pod, color='black', linestyle='--')

    #plt.axhline(y=average_ms, color='r', linestyle='--', label=f'Average ({average_ms:.2f} ms)')
    #plt.axhline(y=median_ms, color='g', linestyle='--', label=f'Median ({median_ms} ms)')
    #plt.axhline(y=std_dev_ms, color='b', linestyle='--', label=f'Standard Deviation ({std_dev_ms:.2f} ms)')
    #plt.fill_between(range(iterations), average_ms - std_dev_ms, average_ms + std_dev_ms, color='gray', alpha=0.3, label='SD Range')

    plt.legend(handles=[
        plt.Line2D([0], [0], color='blue', marker='o', label='Total Duration of Migration'),
        plt.Line2D([0], [0], color='orange', marker='o', label='Pod Downtime'),
        plt.Line2D([0], [0], color='white', marker='', label=f'Average Migration Time: {average_duration:.0f}ms'),
        plt.Line2D([0], [0], color='white', marker='', label=f'Average Pod Downtime: {average_pod:.0f}ms'),
        plt.Line2D([0], [0], color='white', marker='', label=f'Iterations: {iterations}')],
        bbox_to_anchor=(0.5, 1.15), loc='lower center', ncol=3)


    plt.grid(axis="y")
    plt.tight_layout()
    
    savefile = 'C:/Users/rinik/OneDrive/Desktop/ZHAW/07_HS23/PA/ContMigration/data_processing/plots/scatterplot.pdf'
    print(savefile)

    plt.savefig(savefile)
    
    plt.show()
    
def create_hist_plot(data1, data2, data3, title):  
    mu1, std1 = norm.fit(data1)
    mu2, std2 = norm.fit(data2)
    mu3, std3 = norm.fit(data3)

    
    bins = np.arange(0, 35000, 5000)

    #plt.hist(data1, edgecolor="black", bins=bins, label = "Disk Read Write Kill-First", align = "left")
    #plt.hist(data2, edgecolor="black", bins=bins, label = "Mem Intensive Kill-First", align = "mid")
    #plt.hist(data3, edgecolor="black", bins=bins, label = "Mem Intensive Replicate-First", align = "right")
       
    plt.hist([data2, data1, data3], 
             bins, 
             label=['Memory Kill-First',
                    'Disk Read Write Kill-First',                     
                    'Memory Replicate-First'])
    plt.legend(loc='upper right', fontsize='large')
    
    plt.title(title, fontsize='x-large')
    plt.xlabel("Time of Migration [ms]", fontsize='large')
    plt.ylabel("Amount of Migrations", fontsize='large')
    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')
    plt.grid(axis="y")
    
    savefile = 'C:/Users/rinik/OneDrive/Desktop/ZHAW/07_HS23/PA/ContMigration/data_processing/plots/histogram.pdf'
    plt.savefig(savefile, dpi=450)
    plt.show()
    


file_dir_mem = "C:/Users/rinik/OneDrive/Desktop/ZHAW/07_HS23/PA/ContMigration/mem_intensive/data/"
file_dir_drw = "C:/Users/rinik/OneDrive/Desktop/ZHAW/07_HS23/PA/ContMigration/disk_rw_intensive/data/"

path_m_mem_kf = file_dir_mem + "migration_duration_kill_first.txt"
path_d_mem_kf = file_dir_mem + "pod_downtime_kill_first.txt"
data_m_mem_kf = read_data(path_m_mem_kf)
data_d_mem_kf = read_data(path_d_mem_kf)

path_m_mem_rf = file_dir_mem + "migration_duration_replicate_first.txt"
path_d_mem_rf = file_dir_mem + "pod_downtime_replicate_first.txt"
data_m_mem_rf = read_data(path_m_mem_rf)
data_d_mem_rf = read_data(path_d_mem_rf)

path_m_drw_kf = file_dir_drw + "migration_duration_mongo_kill_first.txt"
path_d_drw_kf = file_dir_drw + "pod_downtime_mongo_kill_first.txt"
data_m_drw_kf = read_data(path_m_drw_kf)
data_d_drw_kf = read_data(path_d_drw_kf)

path_m_mem_kf_local = file_dir_mem + "migration_duration_kill_first_local.txt"
path_d_mem_kf_local = file_dir_mem + "pod_downtime_kill_first_local.txt"
data_m_mem_kf_local = read_data(path_m_mem_kf_local)
data_d_mem_kf_local = read_data(path_d_mem_kf_local)

path_m_mem_rf_local = file_dir_mem + "migration_duration_replicate_first_local.txt"
path_d_mem_rf_local = file_dir_mem + "pod_downtime_replicate_first_local.txt"
data_m_mem_rf_local = read_data(path_m_mem_rf_local)
data_d_mem_rf_local = read_data(path_d_mem_rf_local)

path_m_drw_kf_local = file_dir_drw + "migration_duration_mongo_kill_first_local.txt"
path_d_drw_kf_local = file_dir_drw + "pod_downtime_mongo_kill_first_local.txt"
data_m_drw_kf_local = read_data(path_m_drw_kf_local)
data_d_drw_kf_local = read_data(path_d_drw_kf_local)


data_migr1 = data_m_drw_kf
data_migr2 = data_m_mem_kf
data_migr3 = data_m_mem_rf


data_pod = data_d_drw_kf_local
title = "Migration Duration for tested techniques"

#create_scatter_plot(filter_data(data_migr), filter_data(data_pod), title)
#data.sort()
#data_migr.sort()
data_pod.sort()
#create_scatter_plot(filter_data(data_migr), filter_data(data_pod), title)
create_hist_plot(filter_data(data_migr1), filter_data(data_migr2), filter_data(data_migr3), title)
