from tools import *

from scipy.stats import poisson, binom
import os
import timeit
import sys
sys.path.append("../../Task_2/src/")
from algo_bench import *
from algo_bench_mtg import *
import psutil
from mpi4py import MPI 
#from oawidgets.mtg import *

import timeit
def f():
    for x in range(10000):
       x+=1

def distributed_tree_traversal(g,algo,direction,c_pu,t_size=0,alpha=0.4):
    ''' Traversing the tree in a distributed way, were the work is distributed based on the clustering algorithm used
        :Parameterers:
        -   'g' The tree we want to traverse
        -   'algo' The algorithm used to cluster the nodes of the tree
        -   'alpha' Parameter to control the difference between cluster sizes, default value 0.4
        :Returns:
            Nothing
    '''
    MPI.Is_initialized()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    dict_result = {}
    recv_results = {}
    start = MPI.Wtime()
    if rank == 0:
        nb_cpus = c_pu
        if g.property('cluster') != {}:
            g.remove_property('cluster')
        if g.property('sub_tree') != {}:
            g.remove_property('sub_tree')
        if g.property('connection_nodes') != {}:
            g.remove_property('connection_nodes')
        if g.max_scale() - 1 !=  0:
            g.remove_scale(g.max_scale()-1)
        
        algos = [Best_Fit_Clustering_Paper,First_Fit_Clustering_Paper,Best_Fit_Clustering_Queue_1,Best_Fit_Clustering_level_order,First_Fit_Clustering_level_order,Best_Fit_Clustering_Paper_MTG,First_Fit_Clustering_Paper_MTG,Best_Fit_Clustering_post_order_MTG,Best_Fit_Clustering_level_order_MTG]
        start = MPI.Wtime()
        if algo in algos:
            
            if algo != First_Fit_Clustering_Paper and algo != First_Fit_Clustering_Paper_MTG :
                algo(g,nb_cpus,alpha)
            else:
                algo(g,nb_cpus)
            sub_tree = g.property('sub_tree')
            connection_nodes = g.property('connection_nodes')
            for node in sub_tree:
                if g.parent(node) != None:
                    connection_nodes[g.parent(node)] = True
            g.insert_scale(g.max_scale(), lambda vid: vid in sub_tree and vid != None)
        
        else:
            
            raise ("Wrong algorithm try one of these ",algos)
        end = MPI.Wtime()
        print("Using algorithm ",algo.__name__,"------------------------------------------")
        
        print("Time it take to partition the tree using ",algo.__name__,end -start)
        
    else:
        my_mtg = None

    start_1 = MPI.Wtime()
    my_mtg = comm.bcast(g,root=0)
    cluster = my_mtg.property('cluster')
    sub_tree = my_mtg.property('sub_tree')
    connection_nodes = my_mtg.property('connection_nodes')
    for node in sub_tree:
        if my_mtg.parent(node) != None:
            connection_nodes[my_mtg.parent(node)] = True
   
    
    
    if rank != 0 and rank < c_pu:
        for node in my_mtg.vertices(scale=my_mtg.max_scale()-1):
            max_scale_id = my_mtg.component_roots(node)[0]
            if cluster[max_scale_id] == rank:
                if my_mtg.is_leaf(node):
                    for vid in post_order(my_mtg,max_scale_id):
                        f()
                        dict_result[vid] = 1 + sum([dict_result[v_id] for v_id in my_mtg.children(vid)])
                        if vid == max_scale_id:
                            msg = dict_result[max_scale_id]
                            req = comm.isend(msg,dest = cluster[my_mtg.parent(max_scale_id)],tag = max_scale_id)
                                    
                else:
                    for vid in post_order2(my_mtg,max_scale_id,pre_order_filter = lambda v: v not in sub_tree):
                        if vid in connection_nodes:
                            f()
                            dict_result[vid] = 1
                            for child in my_mtg.children(vid):         
                                if cluster[child] != rank:
                                    req = comm.irecv(source = cluster[child],tag = child)
                                    msg = req.wait()
                                    dict_result[vid] += msg
                                else:
                                    dict_result[vid] += dict_result[child]
                            if vid == max_scale_id:
                                msg = dict_result[vid]
                                req = comm.isend(msg,dest = cluster[my_mtg.parent(vid)],tag = vid)
                        else:
                            f()
                            dict_result[vid] = 1 + sum([dict_result[v_id] for v_id in my_mtg.children(vid)])
                            if vid == max_scale_id:
                                msg = dict_result[vid]
                                req = comm.isend(msg,dest = cluster[my_mtg.parent(vid)],tag = vid)

    elif rank == 0:
        for node in my_mtg.vertices(scale=my_mtg.max_scale()-1):
            max_scale_id = my_mtg.component_roots(node)[0]
            if cluster[max_scale_id] == rank:
                for vid in post_order2(my_mtg,max_scale_id,pre_order_filter = lambda v: v not in sub_tree):
                    if vid in connection_nodes:
                        f()
                        dict_result[vid] = 1
                        for child in my_mtg.children(vid):
                            if cluster[child] != rank:
                                req = comm.irecv(source = cluster[child],tag = child)
                                msg = req.wait()
                                dict_result[vid] += msg
                            else:
                                dict_result[vid] += dict_result[child]
                    else:
                        f()
                        dict_result[vid] = 1 + sum([dict_result[v_id] for v_id in my_mtg.children(vid)])
    else:
        dict_result = {}
    comm.Barrier()
    end_1 = MPI.Wtime()
    start_2 = MPI.Wtime()
    
    if rank == 0:
        for node in my_mtg.vertices(scale=my_mtg.max_scale()-1):
            max_scale_id = my_mtg.component_roots(node)[0]
            if cluster[max_scale_id] == rank:
                for vid in pre_order2_with_filter(my_mtg,max_scale_id,pre_order_filter = lambda v: v not in sub_tree):
                    if my_mtg.parent(vid) == None:
                        f()
                        dict_result[vid] = 1
                    else:
                        f()
                        dict_result[vid] = 1 + dict_result[my_mtg.parent(vid)]
                    if vid in connection_nodes:
                        for child in my_mtg.children(vid):
                            if cluster[child] != rank:
                                msg = dict_result[vid]
                                req = comm.isend(msg,dest = cluster[child], tag = child)
    elif rank != 0 and rank < c_pu:
        for node in my_mtg.vertices(scale=my_mtg.max_scale()-1):
            max_scale_id = my_mtg.component_roots(node)[0]
            if cluster[max_scale_id] == rank:
                req = comm.irecv(source = cluster[my_mtg.parent(max_scale_id)],tag = max_scale_id)
                msg = req.wait()
                dict_result[my_mtg.parent(max_scale_id)] = msg
                for vid in pre_order2_with_filter(my_mtg,max_scale_id,pre_order_filter = lambda v: v not in sub_tree):
                    f()
                    dict_result[vid] = 1 + dict_result[my_mtg.parent(vid)]
                    if vid in connection_nodes:
                        for child in my_mtg.children(vid):
                            if cluster[child] != rank:
                                msg = dict_result[vid]
                                req = comm.isend(msg,dest = cluster[child],tag = child)
                        
    else:
        dict_result = {}
    data = comm.gather(dict_result,root=0)
    
    comm.Barrier()
    end_2 = MPI.Wtime()
    if rank == 0:
        print("Using algorithm ",algo.__name__,"------------------------------------------")
        print("Time it took for MPI ",end_1 - start_1,"with direction bottom up"," with ",c_pu,"workers")
        print("Time it took for MPI ",end_2 - start_2,"with direction top down"," with ",c_pu,"workers")
        
        for element in data:
            recv_results.update(element)
        
       

       
        
        

        
    
    


    

            




