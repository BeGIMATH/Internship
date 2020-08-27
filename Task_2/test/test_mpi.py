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

def f_unc():
    for x in range(10000):
       x+=1

algos = [Best_Fit_Clustering,First_Fit_Clustering, Best_Fit_Clustering_post_order, Best_Fit_Clustering_level_order]
t_size = 99999

nb_cpus = [8,16,32,64,128]
#nb_cpus=[4]
nb_tries = 100
for i in range(nb_tries):
    my_mtg = MTG()
    np.random.seed(seed = i)
    dist = poisson(1., loc=1).rvs         
    vid = my_mtg.add_component(my_mtg.root)
    random_tree(my_mtg,vid,nb_children=dist,nb_vertices=t_size)
    for j in range(len(nb_cpus)):
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
                    if algo != First_Fit_Clustering :
                        algo(my_mtg,nb_cpus[j],0.4)
                    else:
                        algo(my_mtg,nb_cpus[j])
               
                
                else:
                    raise ("Wrong algorithm try one of these ",algos)
                
                end = MPI.Wtime()
                print("Partitoning finished for ",algo.__name__," is", end-start,"\n")
                if path.exists('../data/results/' + algo.__name__ + '_partition_time.npy'):
                    with open('../data/results/' + algo.__name__ + '_partition_time.npy','rb') as f:
                        data = np.load(f)

                    data[i,j] = end - start
                    with open('../data/results/' + algo.__name__ + '_partition_time.npy','wb') as f1:
                        np.save(f1,data)      
                else:
                    data = np.zeros([nb_tries,len(nb_cpus)])
                    data[i,j] = end - start
                    with open('../data/results/' + algo.__name__ + '_partition_time.npy','wb') as f1:
                        np.save(f1,data) 
                
                if path.exists('../data/results/' + algo.__name__ + '_longest_path.npy'):
                    with open('../data/results/' + algo.__name__ + '_longest_path.npy','rb') as f:
                        data = np.load(f)
                    #T.insert_scale(T.max_scale(), lambda vid: vid in sub_tree and vid != None)

                    data[i,j] = longest_path(my_mtg,nb_cpus[j])
                    with open('../data/results/' + algo.__name__ + '_longest_path.npy','wb') as f1:
                        np.save(f1,data)      
                else:
                    data = np.zeros([nb_tries,len(nb_cpus)])
                    data[i,j] = longest_path(my_mtg,nb_cpus[j])
                    with open('../data/results/' + algo.__name__ + '_longest_path.npy','wb') as f1:
                        np.save(f1,data) 

                

                
                print("Finished writting data to files\n")
                print("---------------------------------------------------------------\n")
            comm.Barrier()
           
                
            distributed_tree_traversal_bottom_up(my_mtg,algo,j,f_unc,i,nb_tries)   
            distributed_tree_traversal_top_down(my_mtg,algo,j,f_unc,i,nb_tries) 
         



