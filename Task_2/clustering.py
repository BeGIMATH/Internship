from openalea.mtg.mtg import *
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scoop import futures, shared
from itertools import cycle
import numpy as np 


class Priority_queue:
    def __init__(self,weight):
        self.heapList = [0]
        self.currentSize = 0
        self.weight = weight

    def is_not_Empty(self):
        return self.currentSize != 0

    def percUp(self,i):
        while i // 2 > 0:
            if self.weight[self.heapList[i]] < self.weight[self.heapList[i // 2]]:
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
def BF(T):
    pass
  
def SFC_BF(T,p):
    #Initializa the cluster
    C = [[] for i in range(p)]
    remain = np.zeros(p)
    target = 0     
    
    for i in range(1,p):
        target = c + remain[i-1]
        remain[i] = target 
        while(len(C[i]) < (1 - alpha/2)*target):
            #Find the best subtree
            tree = BF(T)
            #Delet the best subtree from the given tree
            T = T - tree 
            #Add those nodes to the cluster
            C[i-1] = C[i-1] + tree
            remain[i] = remain[i] - len(tree)
    return C 





"""
#Algorithm 2
"""

#Clustering using post order traversak with priority queu
def SFC_FF(tree,p):
    vtx_id = tree.root
    C = [[] for i in range(p)]
    
    
    weight = np.zeros(len(tree))
    for v in post_order(tree,tree.root):
        weight[v] = 1 + sum([weight[vid] for vid in tree.children(v)])
    visited = set([])
    #Post order using a priority queue
    queue = Priority_queue(weight)
    queue.append(vtx_id)
    
    while queue.is_not_Empty():
        import pdb as pd 
        pd.set_trace()
        
        vtx_id = queue.last()
        
        for vid in tree.children(vtx_id):
            print(vid)
            if vid not in visited:
                queue.append(vid)
                break
        else: # no child or all have been visited
            yield vtx_id
            visited.add(vtx_id)
            queue.pop()

Mtg = MTG()
my_mtg  = simple_tree(Mtg, Mtg.root,nb_children = 4, nb_vertices=100)

print(list(SFC_FF(my_mtg,10)))

print(list(post_order2(my_mtg, Mtg.root)))


