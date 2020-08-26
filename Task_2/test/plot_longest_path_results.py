from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scipy.stats import poisson, binom
import os
import timeit
import sys
import sys

sys.path.append("../../Task_2/src/")

from algo_clustering import *
from algo_distributed_mpi import *
from IPython.display import HTML
from IPython.display import IFrame
from mpi4py import MPI
import timeit

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

import numpy as np 
import matplotlib.pyplot as plt

cores = [8,16,32,64,128]

algos = [Best_Fit_Clustering,First_Fit_Clustering, Best_Fit_Clustering_post_order, Best_Fit_Clustering_level_order]

algo_data = [[] for i in range(p)]

for i in range(len(algos)):
    with open('../data/results/' + algos[i].__name__ + '_longest_parth.npy','rb') as f:
        algo_data[i] = np.load(f)


best_fit_longest_path = [np.mean(algo_data[0],axis=0)]

first_fit_longest_path = [np.mean(algo_data[1],axis=0)]

best_fit_post_longest_path = [np.mean(algo_data[2],axis=0)]

best_fit_level_longest_path = [np.mean(algo_data[3],axis=0)]


labels = ['8', '16', '32', '64', '128']
x = np.arange(len(labels))
width = 0.3

fig, ax = plt.subplots()

rects1 = ax.bar(x - width, best_fit_longest_path,width/2,label='Algo_1-best-fit')
rects2 = ax.bar(x - width/2, first_fit_longest_path,width/2,label='Algo_1-first-fit')
rects3 = ax.bar(x , best_fit_post_order_longest_path,width/2,label='Algo_2')
rects4 = ax.bar(x + width/2, best_fit_level_order_longest_path,width/2,label='Algo_3')

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')



# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Seconds')
ax.set_xlabel('Workers')
ax.set_title('Longest path size')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


plt.show()
