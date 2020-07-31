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


def f():
    for x in range(100000):
        x+=1

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
    start = MPI.Wtime()
    if rank == 0:
        my_mtg = g#.copy()
        nb_cpus = size
        if my_mtg.property('cluster') != {}:
            my_mtg.remove_property('cluster')
        if my_mtg.property('sub_tree') != {}:
            my_mtg.remove_property('sub_tree')
        if my_mtg.property('connection_nodes') != {}:
            my_mtg.remove_property('connection_nodes')
        if my_mtg.max_scale() - 1 !=  0:
            my_mtg.remove_scale(my_mtg.max_scale()-1)
        algos = [Best_Fit_Clustering_Paper,Best_Fit_Clustering_Queue,First_Fit_Clustering_Paper,Best_Fit_Clustering_Queue_1,Best_Fit_Clustering_level_order]
        if algo in algos:
            if algo != First_Fit_Clustering_Paper:
                algo(my_mtg,nb_cpus,alpha)
            else:
                algo(my_mtg,nb_cpus)
            sub_tree = my_mtg.property('sub_tree')
            
            plot_clusters_dependecy(my_mtg,nb_cluster=nb_cpus,file_name = algo.__name__ + '_dependecy')
            #plot_clusters_dict(my_mtg,nb_cluster = nb_cpus, file_name = algo.__name__ + 'full_plot')
            
            my_mtg.insert_scale(my_mtg.max_scale(), lambda vid: vid in sub_tree and vid != None)
            #print("My vertices at new scale",my_mtg.vertices(scale=my_mtg.max_scale()-1))
        else:
            #Implement a raise error
            print("Wrong algorithm try one of them ",algos)
            
    else:
        my_mtg = None

    
    
    my_mtg = comm.bcast(my_mtg,root=0)
    cluster = my_mtg.property('cluster')
    sub_tree = my_mtg.property('sub_tree')
    connection_nodes = my_mtg.property('connection_nodes')
    for node in sub_tree:
        if my_mtg.parent(node) != None:
            connection_nodes[my_mtg.parent(node)] = True
   
    
    if direction == "bottom_up":
        if rank != 0:
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

        else:
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
    elif direction == "top_down":
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
        else:
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
                        

    data = comm.gather(dict_result,root=0)
           
    end = MPI.Wtime()
    comm.Barrier()
    if rank == 0:
        print("Time it took for MPI ",end - start," using algorithm ",algo.__name__,"direction ",direction)
        for element in data:
            recv_results.update(element)
        
       

       
        
        

        
    
    


    

            




