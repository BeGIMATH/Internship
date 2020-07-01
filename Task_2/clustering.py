from openalea.mtg.mtg import *
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scoop import futures, shared
from itertools import cycle
import numpy as np 
import math

class Priority_queue:
    def __init__(self,weight):
        self.heapList = [0]
        self.currentSize = 0
        self.weight = weight

    def is_not_Empty(self):
        return self.currentSize != 0

    def percUp(self,i):
        while i // 2 > 0:
            if self.weight[self.heapList[i]] > self.weight[self.heapList[i // 2]]:
                #Swap places
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp 
            i = i // 2
    
    def append(self,x):
        #Insert the element at the end of the list 
        self.heapList.append(x)
        #Increment the size variable
        self.currentSize = self.currentSize + 1 
        #Place the element based on its size
        self.percUp(self.currentSize)
    
    def pop(self):
        retval = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        return retval
    
    def last(self):
        #Return the last element without removing from the queue
        retval = self.heapList[self.currentSize]
        return retval

"""
#Algorithm 1
"""
### To be done ###

def change_parent(node):
    dict[T.parent(node)] -= size 
  
def SFC_BF(T,p,alpha):
    #Initializa the cluster
    C = [[] for i in range(p)]     
    weight = np.zeros(len(T))
    for v in post_order(T,T.root):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    node_dict = {i:weight[i] for i in range(len(T))}
    sub = 0
    target = len(T)/p
    maxima = 0
    for i in range(p): 
        for key in node_dict:
            maxima = max(maxima,node_dict[key])
            sub = key
            if maxima + 1 > target:
                sub = key
                break 
        print("Nodes for a given subtree")
        for node in T.sub_tree(sub,False):
            
            node_dict.pop(node)
        C[i].append(list(T.sub_tree(sub)))
        
        node = sub 
        while T.parent(node):
            node_dict[T.parent(node)] -= node_dict[node]   
            node = T.parent(node)
        
    return C 





"""
#Algorithm 2
"""

#Clustering using post order traversal with priority queu
def SFC_FF(tree,p,c):
    vtx_id = tree.root
    C = [[] for i in range(p)]
    
    
    weight = np.zeros(len(tree))
    for v in post_order(tree,tree.root):
        weight[v] = 1 + sum([weight[vid] for vid in tree.children(v)])
    visited = set([])
    #Post order using a priority queue
    queue = Priority_queue(weight)
    queue.append(vtx_id)
    counter = 0
    while queue.is_not_Empty():
        vtx_id = queue.last()
        
        for vid in tree.children(vtx_id):
            if vid not in visited:
                queue.append(vid)
                break
        else: # no child or all have been visited
            counter += 1
            visited.add(vtx_id)
            queue.pop()
            C[math.floor(counter/c)].append(vtx_id)
    return C

from scipy.stats import poisson, binom 

my_mtg = MTG()
dist = poisson(1., loc=1).rvs
random_tree(my_mtg,my_mtg.root, nb_children=dist,nb_vertices=99)
#my_mtg  = simple_tree(Mtg, Mtg.root,nb_children = 4, nb_vertices=100)

clusters = SFC_FF(my_mtg,10,11)
clusters1 = SFC_BF(my_mtg,10,0.4)


