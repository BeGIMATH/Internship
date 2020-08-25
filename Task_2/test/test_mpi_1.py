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

from algo_bench_mtg import *
from algo_distributed_mpi import *
from IPython.display import HTML
from IPython.display import IFrame
from mpi4py import MPI
import timeit



algos = [Best_Fit_Clustering_Paper_MTG,First_Fit_Clustering_Paper_MTG,Best_Fit_Clustering_post_order_MTG,Best_Fit_Clustering_level_order_MTG]

nb_cpus = [4,6]

for c_pu in nb_cpus:
    for algo in algos:
        distributed_tree_traversal(algo,"bottom_up",c_pu)   
        #distributed_tree_traversal(test_mtg,algo,"top_down",c_pu)


