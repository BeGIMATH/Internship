from Queue import *

from scipy.stats import poisson, binom
import os
import timeit
import sys
sys.path.append("../../Task_2/src/")
from algo_bench import *
from mpi4py import MPI 
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
dict_result = {}
recv_results = {}
import psutil


def bottom_up():
    pass

def top_down():
    pass


def distributed_traversal(g,algo,direction,alpha=0.4):
    if rank == 0:
        nb_cpus = psutil.cpu_count(logical=False)
        
        algos = ["Best_Fit_Clustering_Paper","Best_Fit_Clustering_Queue","First_Fit_Clustering_Paper","Best_Fit_Clustering_Queue_1","Best_Fit_Clustering_No_Queue","Best_Fit_Clustering_No_Queue_1"]
        if algo in algos:
            if algo != "First_Fit_Clustering_Paper":
                algo(g,nb_cpus,alpha)
            else:
                algo(g,nb_cpus)

            g.insert_scale(g.max_scale(), lambda vid: g.property('sub_tree').get(vid,None) != None)
            connection_nodes = my_mtg.property('connection_nodes')
            for node in my_mtg.property('sub_tree'):
                if my_mtg.parent(node) != None:
                    connection_nodes[node] = True
            
            my_mtg = g
        
        else:
            #Implement a raise error
            print("Wrong algorithm try one of them ",algos)
            
    
    else:
        my_mtg = None

    my_mtg = comm.bcast(my_mtg,root=0)
    cluster = my_mtg.property('cluster')
    sub_tree = my_mtg.property('sub_tree')
    dict_result = {}
    if direction == "bottom_up":
        if rank != 0:
            for node in my_mtg.vertices(scale=my_mtg.max_scale()-1):
                if cluster[my_mtg.component_roots(node)[0]] == rank:
                    if my_mtg.children(node) == None:
                        for vid in post_order2_with_filter(my_mtg.component_roots(node)[0],pre_order_filter = lambda v: v not in sub_tree):
                            if vid == my_mtg.component_roots(node)[0]:
                                msg = 'start'
                                req = comm.isend(msg,dest = cluster[my_mtg.parent(vid)],my_mtg.parent(vid))
                            dict_result[vid] = dummy_function(vid)
                    
                    else:
                        for vid in post_order2_with_filter(my_mtg.component_roots(node)[0],pre_order_filter = lambda v: v not in sub_tree):
                            if vid in connection_nodes:
                                for child in my_mtg.children(vid):        
                                    if cluster[child] != rank:
                                        req = comm.irecv(source = cluster[child],tag = child)
                                        msg = req.wait()
                                        if msg == 'start':
                                            dict_result[child] = dummy_function(child)
                
                            dict_result[vid] = dummy_function(vid)


        else:
            for node in my_mtg.vertices(scale=my_mtg.max_scale()):
                if cluster[my_mtg.component_roots(node)[0]] == rank:
                    for vid in post_order2_with_filter(my_mtg.component_roots(node)[0],pre_order_filter = lambda v: v not in sub_tree):
                        if vid in connection_nodes:
                            for child in my_mtg.children(vid):
                                if cluster[child] != rank:
                                    req = comm.irecv(source = cluster[child],tag = child)
                                    msg = req.wait()
                                    if msg == 'start':
                                        dict_result[child] = dummy_function(child)
                        dict_result[vid] = dummy_function(vid)


        if rank!= 0:
            comm.send(dict_result,dest=0,tag=1)
        else:
            for i in range(1,size):
                dict_result = comm.recv(source = i,tag=1)
                recv_results.update(dict_result)
    elif:
        direction == "top_down":
        if rank == 0:
            for node in sub_tree:
                if cluster[node] == rank:
                for vid in pre_order2_with_filter(my_mtg,node,pre_order_filter = lambda v: v not in sub_tree):
                    if vid in connection_nodes:
                        for child in my_mtg.children(vid):
                            if cluster[child] != rank:
                                msg = 'start'
                                req = comm.isend(msg,dest = cluster[child], tag = child)
                    dict_result[vid] = dummy_function(vid)                       
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



    

            




