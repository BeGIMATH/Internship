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

algo_data = [[] for i in range(len(algos))]

for i in range(len(algos)):
    with open('../data/results/' + algos[i].__name__ + '_top_down.npy','rb') as f:
        algo_data[i] = np.load(f)


best_fit_top_down = np.mean(algo_data[0],axis=0)

first_fit_top_down = np.mean(algo_data[1],axis=0)

best_fit_post_order_top_down = np.mean(algo_data[2],axis=0)

best_fit_level_order_top_down = np.mean(algo_data[3],axis=0)


labels = ['8', '16', '32', '64', '128']
x = np.arange(len(labels))
width = 0.3

fig, ax = plt.subplots()
"""
rects1 = ax.bar(x - width, best_fit_top_down,width/2,label='Algo_1-best-fit')
rects2 = ax.bar(x - width/2, first_fit_top_down,width/2,label='Algo_1-first-fit')
rects3 = ax.bar(x , best_fit_post_order_top_down,width/2,label='Algo_2')
rects4 = ax.bar(x + width/2, best_fit_level_order_top_down,width/2,label='Algo_3')
"""
ax2 = ax.twinx()
def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)



algo_0_box = ax2.boxplot(algo_data[0],positions = [0-width,1-width,2-width,3-width,4-width], widths=0.09)
algo_1_box = ax2.boxplot(algo_data[1],positions = [0-width/2,1-width/2,2-width/2,3-width/2,4-width/2],widths=0.09)
algo_2_box = ax2.boxplot(algo_data[2],positions = [0,1,2,3,4],widths=0.09)
algo_3_box = ax2.boxplot(algo_data[3],positions = [0+width/2,1+width/2,2+width/2,3+width/2,4+width/2],widths=0.09)

set_box_color(algo_0_box, 'red') # colors are from http://colorbrewer2.org/
set_box_color(algo_1_box, 'blue')


set_box_color(algo_2_box, 'orange') # colors are from http://colorbrewer2.org/
set_box_color(algo_3_box, 'green')

ax.plot([], c='red', label='Algo_1_best_fit')
ax.plot([], c='blue', label='Algo_1_first_fit')


ax.plot([], c='orange', label='Algo_2')
ax.plot([], c='green', label='Algo_3')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Seconds')
ax.set_xlabel('Workers')
ax.set_title('Root to leaf traversal time')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


plt.show()
