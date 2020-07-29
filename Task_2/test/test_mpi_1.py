from Queue import *

from scipy.stats import poisson, binom
import os
import timeit
import sys
sys.path.append("../../Task_2/src/")
from algo_bench import *
import psutil
from mpi4py import MPI 
from oawidgets.mtg import *


def dummy_function(x):
    return x

def distributed_tree_traversal(g,algo,direction,alpha=0.4):
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

    if rank == 0:
        my_mtg = g.copy()
        nb_cpus = psutil.cpu_count(logical=False)
        
        algos = [Best_Fit_Clustering_Paper,Best_Fit_Clustering_Queue,First_Fit_Clustering_Paper,Best_Fit_Clustering_Queue_1,Best_Fit_Clustering_level_order]
        if algo in algos:
            if algo != First_Fit_Clustering_Paper:
                algo(my_mtg,nb_cpus,alpha)
            else:
                algo(my_mtg,nb_cpus)
            sub_tree = my_mtg.property('sub_tree')
            plot_clusters_dependecy(my_mtg,nb_cluster=nb_cpus,file_name = algo.__name__ + '_dependecy')
            plot_clusters_dict(my_mtg,nb_cluster = nb_cpus, file_name = algo.__name__ + 'full_plot')
            
            my_mtg.insert_scale(my_mtg.max_scale(), lambda vid: vid in sub_tree)
            connection_nodes = my_mtg.property('connection_nodes')
            for node in sub_tree:
                if my_mtg.parent(node) != None:
                    connection_nodes[node] = True
        else:
            #Implement a raise error
            print("Wrong algorithm try one of them ",algos)
            
    else:
        my_mtg = None

    start = MPI.Wtime()
    
    my_mtg = comm.bcast(my_mtg,root=0)
    cluster = my_mtg.property('cluster')
    sub_tree = my_mtg.property('sub_tree')
    
   
    
    if direction == "bottom_up":
        connection_nodes = my_mtg.property('connection_nodes')
        for node in sub_tree:
            if my_mtg.parent(node) != None:
                connection_nodes[my_mtg.parent(node)] = True
        if rank != 0:
            for node in my_mtg.vertices(scale=my_mtg.max_scale()-1):
                max_scale_id = my_mtg.component_roots(node)[0]
                if cluster[max_scale_id] == rank:
                    if my_mtg.is_leaf(node):
                        for vid in post_order(my_mtg,max_scale_id):
                            dict_result[vid] = 1 + sum([dict_result[v_id] for v_id in my_mtg.children(vid)])
                            if vid == max_scale_id:
                                msg = dict_result[max_scale_id]
                                req = comm.isend(msg,dest = cluster[my_mtg.parent(max_scale_id)],tag = max_scale_id)
                                    
                    else:
                        for vid in post_order2(my_mtg,max_scale_id,pre_order_filter = lambda v: v not in sub_tree):
                            if vid in connection_nodes:
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
                                dict_result[vid] = 1 + sum([dict_result[v_id] for v_id in my_mtg.children(vid)])
                                if vid == max_scale_id:
                                    msg = dict_result[vid]
                                    req = comm.isend(msg,dest = cluster[my_mtg.parent(vid)],tag = vid)

        else:
                max_scale_id = my_mtg.component_roots(my_mtg.root)[0]
                for vid in post_order2(my_mtg,max_scale_id,pre_order_filter = lambda v: v not in sub_tree):
                    if vid in connection_nodes:
                        dict_result[vid] = 1
                        for child in my_mtg.children(vid):
                            if cluster[child] != rank:
                                req = comm.irecv(source = cluster[child],tag = child)
                                msg = req.wait()
                                dict_result[vid] += msg
                            else:
                                dict_result[vid] += dict_result[child]
                    else:
                        dict_result[vid] = 1 + sum([dict_result[v_id] for v_id in my_mtg.children(vid)])
    elif direction == "top_down":
        if rank == 0:
            for node in sub_tree:
                if cluster[node] == rank:
                    for vid in pre_order2_with_filter(my_mtg,node,pre_order_filter = lambda v: v not in sub_tree):
                        if vid in connection_nodes:
                            for child in my_mtg.children(vid):
                                if cluster[child] != rank:
                                    msg = 'start'
                                    req = comm.isend(msg,dest = cluster[child], tag = child)
                        dict_result[vid] = dummy_function(my_mtg.parent(vid))                       
        else:
            for node in sub_tree:
                if cluster[node] == rank:
                    req = comm.irecv(source = cluster[my_mtg.parent(node)],tag = node)
                    msg = req.wait()
                    if msg == 'start':
                        for vid in pre_order2_with_filter(my_mtg,node,pre_order_filter = lambda v: v not in sub_tree):
                            if vid in connection_nodes:
                                for child in my_mtg.children(vid):
                                    if cluster[child] != rank:
                                        msg = 'start'
                                        req = comm.isend(msg,dest = cluster[child],tag = child)
                            dict_result[vid] = dummy_function(vid)

        if rank!= 0:
            comm.send(dict_result,dest=0,tag=1)
        else:
            for i in range(1,size):
                dict_result = comm.recv(source = i,tag=1)
                recv_results.update(dict_result)
           
 
           
            
    
    end = MPI.Wtime()
    comm.Barrier()
    if rank == 0:
        print("Time it take for MPI ",end - start)
        
        

        
    
    


    

            




