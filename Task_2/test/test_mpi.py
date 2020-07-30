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

test_mtg = MTG()#'../data/noylum2.mtg')
dist = poisson(1., loc=1).rvs

vid = test_mtg.add_component(test_mtg.root)

random_tree(test_mtg,vid,nb_children=dist,nb_vertices=999)
algos = [Best_Fit_Clustering_Paper,Best_Fit_Clustering_Queue,First_Fit_Clustering_Paper,Best_Fit_Clustering_Queue_1,Best_Fit_Clustering_level_order]
for algo in algos:
    distributed_tree_traversal(test_mtg,algo,"bottom_up")
    distributed_tree_traversal(test_mtg,algo,"top_down")


def f():
    for x in range(2500):
        x+=1
comm = MPI.COMM_WORLD  
rank = comm.Get_rank()
if rank == 0:
    start = MPI.Wtime()
    dict_result = {}
    for vid in post_order2(test_mtg,vid):
        dict_result[vid] = 1 + sum([dict_result[v_id] for v_id in test_mtg.children(vid)])
        f()
    end = MPI.Wtime()

    print("Time for the sequentail program ",end - start)
                        


