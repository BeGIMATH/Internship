
from openalea.mtg.mtg import *
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scoop import futures, shared
from itertools import cycle
 


def Max_depth_MTG_p_l(node, currentDepth = 0, parallelLevel = 4):
    mtg = shared.getConst('myTree')
    
    
    if currentDepth >= parallelLevel:
        return Max_depth_MTG_serial(node)
    
    else:
        nodes = []
        leafs = []
        # Classify nodes either as leafs or as nodes
        childs = mtg.Sons(node)
        for i in childs:
            if not mtg.Sons(i) == None:
                nodes.append(i)
        
        if len(nodes) == 0:
            return currentDepth
        if len(nodes) == 1:
            return Max_depth_MTG_serial(nodes[0]) + 1
        else:
            return max(futures.map(Max_depth_MTG_p_l,[nodes[i] for i in range(len(nodes))],
            cycle([currentDepth + 1]),
            cycle([parallelLevel]),
             )
        ) + 1
            
        




def Max_depth_MTG_serial(node):
    mtg = shared.getConst('myTree')
    childs = mtg.Sons(node)
    nodes = []
    leafs = []
    #Classify nodes either as leafs or as nodes
    for i in childs:
        if mtg.Sons(i) == None:
            leafs.append(i)
        else:
            nodes.append(i)
    #If the all
    if len(nodes) == 0:
        return 1
    if len(nodes) == 1:
        return Max_depth_MTG_serial(nodes[0]) + 1
    else:
         return max(map(Max_depth_MTG_serial,[nodes[i] for i in range(len(nodes))] )) + 1
         

import operator
import time


if __name__ == '__main__':
    
    Mtg = MTG()
    my_mtg  = simple_tree(Mtg, Mtg.root,nb_children = 4, nb_vertices=1000)
    
    shared.setConst(myTree=my_mtg)
    
    root = my_mtg.roots()[0]
    ts = time.time()
    result_parallel = Max_depth_MTG_p_l(root,parallelLevel=2)
    pts = time.time() - ts
    ts_1 = time.time()
    result_serial = Max_depth_MTG_serial(root)
    sts = time.time() - ts_1
    
    print("The length of the tree in parallel ", result_parallel)
    print("It took ", pts)

    print("The length of the tree in serial", result_serial)
    print("It took ", sts)
    display_tree(my_mtg,0)