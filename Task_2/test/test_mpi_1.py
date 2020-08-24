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


"""
if rank == 0:
   
    start = timeit.default_timer()
    dict_result = {}
    for node in pre_order(test_mtg,vid):
        if test_mtg.parent(node) == None:
            f()
            dict_result[node] = 1
        else:
            dict_result[node] = 1 + dict_result[test_mtg.parent(node)]
            f()
    end = timeit.default_timer()

    print("Time it took for the sequentail program ",end - start,"direction top down")
    
    
    start = timeit.default_timer()
    dict_result_1 = {}
    for node in post_order2(test_mtg,vid):
        dict_result_1[node] = 1 + sum([dict_result_1[v_id] for v_id in test_mtg.children(node)])
        f()
    end = timeit.default_timer()

    print("Time it took for the sequentail program ",end - start,"direction bottom up")
"""
algos = [Best_Fit_Clustering_Paper_MTG,First_Fit_Clustering_Paper_MTG,Best_Fit_Clustering_post_order_MTG,Best_Fit_Clustering_level_order_MTG]

nb_cpus = [4]
test_mtg = MTG('../data/consolidated_mango3d.mtg')

#nb_cpus = [8,16,32,64,128]
for t_size in tree_size:
    for c_pu in nb_cpus:
        for algo in algos:
            distributed_tree_traversal(test_mtg,algo,"bottom_up",c_pu,t_size)   
            distributed_tree_traversal(test_mtg,algo,"top_down",c_pu,t_size)









