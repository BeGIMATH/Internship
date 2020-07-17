from dask.distributed import Client, get_client, secede, rejoin
from dask import delayed, compute
import timeit
from openalea.mtg.mtg import *
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from itertools import cycle


def Max_depth_MTG_p_l(node, currentDepth = 0, parallelLevel = 2):
    client = get_client()
    tree = my_mtg
    
    edge_type = tree.property('edge_type')
    def Max_depth_MTG_serial(vtx_id):
        #mtg = shared.getConst('myTree')
        successor = []
        plus = []
        for i in tree.Sons(vtx_id):
            if edge_type.get(i) == '<':
                successor.append(i)
            else:
                plus.append(i)
        
        if len(successor) + len(plus) == 0:
            return 1
        elif len(successor) + len(plus) > 0:
            if len(successor) > 0:
                return Max_depth_MTG_serial(successor[0]) + 1
            else:
                return max(map(Max_depth_MTG_serial,[plus[i] for i in range(len(plus))] )) + 1

        #Classify nodes either as leafs or as nodes
        else:
            l_max = Max_depth_MTG_serial(successor[0])
            r_max = max(map(Max_depth_MTG_serial,[plus[i] for i in range(len(plus))] ))
            return max(l_max,r_max) + 1
        
    if currentDepth >= parallelLevel:
            return Max_depth_MTG_serial(node)
    
    else:
        successor = []
        plus = []
        for i in tree.Sons(node):
            if edge_type.get(i) == '<':
                successor.append(i)
            else:
                plus.append(i)
        
        if len(successor) == 0:
            if len(plus) == 0:
                return currentDepth
            else:
                l_max = Max_depth_MTG_p_l(plus[0])
                futures = client.map(Max_depth_MTG_p_l,[currentDepth+1],[plus[i] for i in range(1,len(plus))])
                secede()
                results = client.gather(futures)
                rejoin()
                return max(results) + 1
                
        else:
            l_max = Max_depth_MTG_p_l(successor[0])
            futures = client.map(Max_depth_MTG_p_l,[currentDepth+1],[plus[i] for i in range(1,len(plus))])
            secede()
            results = client.gather(futures)
            rejoin()
            r_max = max(results)
            return max(l_max,r_max) + 1




if __name__ == "__main__":
    client = Client()
    #DASK_DISTRIBUTED__SCHEDULER__WORK_STEALING="False"
    my_mtg = MTG()#"/home/begatim/Desktop/Thesis_Project/Practice/mtg/share/data/wij10.mtg")
    my_mtg  = simple_tree(my_mtg,my_mtg.root,nb_children = 4, nb_vertices=1000)
    
    
    ts = timeit.default_timer()
    future = client.submit(Max_depth_MTG_p_l,my_mtg.root,parallelLevel=2)
    result_parallel = future.result()
    
    pts = timeit.default_timer()
    
    
    t = timeit.default_timer()
    l1 = list(pre_order(my_mtg, my_mtg.root))
    t1 = timeit.default_timer()

    print("The length of the tree in parallel ", result_parallel)
    print("It took ", pts - ts)
    
    print("time for implemented traverse func",t1-t )
   
    
   