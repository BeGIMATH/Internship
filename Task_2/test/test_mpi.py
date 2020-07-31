from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scipy.stats import poisson, binom
import os
import timeit
import sys
from oawidgets.mtg import *
from oawidgets.plantgl import PlantGL
from openalea.mtg.draw import *
import sys

sys.path.append("../../Task_2/src/")

from algo_bench import *
from algo_distributed_mpi import *
from oawidgets.mtg import plot
from oawidgets.plantgl import PlantGL
from IPython.display import HTML
from IPython.display import IFrame

from mpi4py import MPI
import timeit
test_mtg = MTG()#'../data/noylum2.mtg')
dist = poisson(1., loc=1).rvs
comm = MPI.COMM_WORLD  
rank = comm.Get_rank()
vid = test_mtg.add_component(test_mtg.root)
simple_tree(test_mtg,vid,nb_children=6,nb_vertices=999)
def f():
    for x in range(100000):
        x+=1

if rank == 0:
   
    start = timeit.default_timer()
    dict_result = {}
    my_mtg = test_mtg.copy()
    for node in pre_order(my_mtg,vid):
        if test_mtg.parent(node) == None:
            f()
            dict_result[node] = 1
        else:
            dict_result[node] = 1 + dict_result[my_mtg.parent(node)]
            f()
    end = timeit.default_timer()

    print("Time it took for the sequentail program ",end - start,"direction top down")
    
    
    start = timeit.default_timer()
    dict_result_1 = {}
    for node in post_order2(my_mtg,vid):
        dict_result_1[node] = 1 + sum([dict_result_1[v_id] for v_id in my_mtg.children(node)])
        f()
    end = timeit.default_timer()

    print("Time it took for the sequentail program ",end - start,"direction bottom up")


    
algos = [Best_Fit_Clustering_Paper,Best_Fit_Clustering_Queue,First_Fit_Clustering_Paper,Best_Fit_Clustering_Queue_1,Best_Fit_Clustering_level_order]
for algo in algos:
    distributed_tree_traversal(test_mtg,algo,"bottom_up")
    distributed_tree_traversal(test_mtg,algo,"top_down")


