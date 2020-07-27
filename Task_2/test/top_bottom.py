from openalea.mtg.draw import *
from oawidgets.plantgl import PlantGL
from oawidgets.mtg import *

from oawidgets.mtg import plot
from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
from openalea.mtg.io import *
from openalea.mtg.traversal import *
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

if rank == 0:
    my_mtg = MTG()

    dist = poisson(1., loc=1).rvs

    vid = my_mtg.add_component(my_mtg.root)

    random_tree(my_mtg, vid, nb_children=dist, nb_vertices=99)
    
    Best_Fit_Clustering_Paper(my_mtg,size,0.4)
    connection_nodes = my_mtg.property('connection_nodes')
    for node in my_mtg.property('sub_tree'):
        if my_mtg.parent(node) != None:
            connection_nodes[node] = True

else:
    my_mtg = None

my_mtg = comm.bcast(my_mtg,root=0)
cluster = my_mtg.property('cluster')
sub_tree = my_mtg.property('sub_tree')

dict_result = {}
if rank == 0:
    for sub_tree_root in sub_tree:
        if cluster[sub_tree_root] == rank:
            for vid in pre_order2_with_filter(my_mtg,sub_tree_root,pre_order_filter = lambda v: v not in sub_tree):
                if vid in connection_nodes:
                    for child in my_mtg.children(vid):
                        if cluster[child] != rank:
                            msg = 'start'
                            req = comm.isend(msg,dest = cluster[child], tag = child)
                dict_result[vid] = dummy_function(vid)                       
else:
    for sub_tree_root in sub_tree:
        if cluster[sub_tree_root] == rank:
            req = comm.irecv(source = cluster[my_mtg.parent(sub_tree_root)],tag = sub_tree_root)
            msg = req.wait()
            if msg == 'start':
                for vid in pre_order2_with_filter(my_mtg,sub_tree_root,pre_order_filter = lambda v: v not in sub_tree):
                    if vid in connection_nodes:
                        for child in my_mtg.children(vid):
                            if cluster[child] != rank:
                                msg = 'start'
                                req = comm.isend(msg,dest = cluster[child],tag = child)
                else:
                    dict_result[vid] = dummy_function(vid)

if rank == 0:
    for i in range(1,size):
        dict_result = comm.recv(source = i,tag=1)
        recv_results.update(dict_result)
    
else:
    comm.send(dict_result,dest=0,tag=1)
    
if rank == 0:
    print("Results ",recv_results)                   
            