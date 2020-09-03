from openalea.parallel_mtg.tools import *

from openalea.parallel_mtg.algo_clustering import *

from mpi4py import MPI 
import numpy as np

def distributed_tree_traversal_bottom_up(g,func):
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
        
        sub_tree = g.property('sub_tree')
        connection_nodes = g.property('connection_nodes')
        for node in sub_tree:
            if g.parent(node) != None:
                connection_nodes[g.parent(node)] = True
        g.insert_scale(g.max_scale(), lambda vid: vid in sub_tree and vid != None)
        
        
    else:
        my_mtg = None

    my_mtg = comm.bcast(g,root=0)
    cluster = my_mtg.property('cluster')
    sub_tree = my_mtg.property('sub_tree')
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
                        func()
                        dict_result[vid] = 1 + sum([dict_result[v_id] for v_id in my_mtg.children(vid)])
                        if vid == max_scale_id:
                            msg = dict_result[max_scale_id]
                            req = comm.isend(msg,dest = cluster[my_mtg.parent(max_scale_id)],tag = max_scale_id)
                                    
                else:
                    for vid in post_order2(my_mtg,max_scale_id,pre_order_filter = lambda v: v not in sub_tree):
                        if vid in connection_nodes:
                            func()
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
                            func()
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
                        func()
                        dict_result[vid] = 1
                        for child in my_mtg.children(vid):
                            if cluster[child] != rank:
                                req = comm.irecv(source = cluster[child],tag = child)
                                msg = req.wait()
                                dict_result[vid] += msg
                            else:
                                dict_result[vid] += dict_result[child]
                    else:
                        func()
                        dict_result[vid] = 1 + sum([dict_result[v_id] for v_id in my_mtg.children(vid)])
                        
    
    comm.Barrier()
    
    data = comm.gather(dict_result,root=0)
    
    
    if rank == 0:
        for element in data:
            recv_results.update(element)
        
        if my_mtg.property('cluster') != {}:
            g.remove_property('cluster')
        if g.property('sub_tree') != {}:
            g.remove_property('sub_tree')
        if g.property('connection_nodes') != {}:
            g.remove_property('connection_nodes')
        if g.max_scale() - 1 !=  0:
            g.remove_scale(g.max_scale()-1)
        
        

def distributed_tree_traversal_top_down(g,algo,c_pu,func,t_index,nb_tries):
    ''' Traversing the tree in a distributed way, were the work is distributed based on the clustering algorithm used
        :Parameterers:
        -   'g' The tree we want to traverse
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
        
        
        sub_tree = g.property('sub_tree')
        connection_nodes = g.property('connection_nodes')
        for node in sub_tree:
            if g.parent(node) != None:
                connection_nodes[g.parent(node)] = True
        g.insert_scale(g.max_scale(), lambda vid: vid in sub_tree and vid != None)
        
       
     
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
    
    if rank == 0:
        for node in my_mtg.vertices(scale=my_mtg.max_scale()-1):
            max_scale_id = my_mtg.component_roots(node)[0]
            if cluster[max_scale_id] == rank:
                for vid in pre_order2_with_filter(my_mtg,max_scale_id,pre_order_filter = lambda v: v not in sub_tree):
                    if my_mtg.parent(vid) == None:
                        func()
                        dict_result[vid] = 1
                    else:
                        func()
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
                    func()
                    dict_result[vid] = 1 + dict_result[my_mtg.parent(vid)]
                    if vid in connection_nodes:
                        for child in my_mtg.children(vid):
                            if cluster[child] != rank:
                                msg = dict_result[vid]
                                req = comm.isend(msg,dest = cluster[child],tag = child)
                        
    
    data = comm.gather(dict_result,root=0)
    
    comm.Barrier()
    end_1 = MPI.Wtime()
    if rank == 0:
        for element in data:
            recv_results.update(element)


        if my_mtg.property('cluster') != {}:
            g.remove_property('cluster')
        if g.property('sub_tree') != {}:
            g.remove_property('sub_tree')
        if g.property('connection_nodes') != {}:
            g.remove_property('connection_nodes')
        if g.max_scale() - 1 !=  0:
            g.remove_scale(g.max_scale()-1)
        
        

        
    
    


    

            



