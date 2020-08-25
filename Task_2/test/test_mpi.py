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

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def f_unc():
    for x in range(10000):
       x+=1

algos = [Best_Fit_Clustering_Paper_MTG,First_Fit_Clustering_Paper_MTG,Best_Fit_Clustering_post_order_MTG,Best_Fit_Clustering_level_order_MTG]
t_size = 99999

for i in range(100):
    my_mtg = MTG()
    np.random.seed(seed = i)
    dist = poisson(1., loc=1).rvs         
    vid = my_mtg.add_component(my_mtg.root)
    random_tree(my_mtg,vid,nb_children=dist,nb_vertices=t_size)
    for j in range(5):
        for algo in algos:
            if rank == 0:
                if my_mtg.property('cluster') != {}:
                    my_mtg.remove_property('cluster')
                if my_mtg.property('sub_tree') != {}:
                    my_mtg.remove_property('sub_tree')
                if my_mtg.property('connection_nodes') != {}:
                    my_mtg.remove_property('connection_nodes')
                if my_mtg.max_scale() - 1 !=  0:
                    my_mtg.remove_scale(my_mtg.max_scale()-1)
                start = MPI.Wtime()
                if algo in algos:
                    if algo != First_Fit_Clustering_Paper_MTG :
                        algo(my_mtg,j,0.4)
                    else:
                        algo(my_mtg,j)
                else:
                    raise ("Wrong algorithm try one of these ",algos)
                end = MPI.Wtime()
                if path.exists('../data/results/' + algo.__name__ + '_partition_time.npy'):
                    with open('../data/results/' + algo.__name__ + '_partition_time.npy','rb') as f:
                        data = np.load(f)

                    data[i,j] = end - start
                    with open('../data/results/' + algo.__name__ + '_partition_time.npy','wb') as f1:
                        np.save(f1,data)      
                else:
                    data = np.zeros([100,5])
                    data[i,j] = end - start
                    with open('../data/results/' + algo.__name__ + '_partition_time','wb') as f1:
                        np.save(f1,data) 

        
                print("Partitoning finished for ",algo.__name__," is", end-start)
            
            comm.Barrier()
           
                
            distributed_tree_traversal_bottom_up(my_mtg,j,f_unc,i)   
            distributed_tree_traversal_top_down(my_mtg,j,f_unc,i) 
         




