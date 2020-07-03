from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scoop import futures, shared
from itertools import cycle
import numpy as np 
import math

class Priority_queue:
    def __init__(self,weight,ordering):
        self.heapList = [0]
        self.currentSize = 0
        self.weight = weight
        self.ordering = ordering

    def Empty(self):
        return self.currentSize == 0

    def percUp(self,i):
        while i // 2 > 0:
            if self.weight[self.heapList[i]] < self.weight[self.heapList[i // 2]]:
                #Swap places
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp 
            i = i // 2
    
    def percDown(self,i):
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
        if self.ordering == "up":
            self.percUp(self.currentSize)
        elif self.ordering == "down":
            self.percDown(self.currentSize)

    def pop(self):
        retval = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        return retval
    
    def last(self):
        #Return the last element without removing from the queue
        retval = self.heapList[self.currentSize]
        return retval
    
    def size(self):
        return self.currentSize

"""
#Algorithm 1
"""
### To be done ###

 
def SFC_BF_DICT(T,p,alpha=0):
    #Initialize the clusters
    C = [[] for i in range(p)]     
    #Create the weight array
    weight = np.zeros(len(T))
    #Traverse the tree in post order to get the node ids
    A = list(post_order(T,T.root))
    #Compute the weights of all the nodes
    for v in A:
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    #Store all the nodes inside the dictionary
    node_dict = {i:weight[i] for i in range(len(T))}
    sub = 0
    target = len(T)/p
    maxima = 0
    for i in range(p): 
        for key in node_dict:
            if weight[T.parent(key)] > remain:
                sub = key
            #maxima = max(maxima,node_dict[key])
            sub = key
            if maxima + 1 > target:
                sub = key
                break 
        print("Nodes for a given subtree")
        
        for node in T.sub_tree(sub,False):
        
            node_dict.pop(node)
        C[i] += list(T.sub_tree(sub))
        
        node = sub 
        while T.parent(node):
            node_dict[T.parent(node)] -= node_dict[node]   
            node = T.parent(node)
        
    return C 

def SFC_BF(T,p,c):
    #Initialize the cluster
    C = [[] for i in range(p)]
    remain = 0
    #Initialize the array of weights
    weight = np.zeros(len(T))

    #Compute the weights for all the nodes
    for v in list(post_order(T,T.root)):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    #Add only one subtree of the given size into the queue
    
    

    def BF(remain,first_time,Q):
        #If the queue is not empty, search for the subtrees inside the queue
        sub = 0
        #Filling the queue for the first time
        sub_tree_size = 0
        
        if first_time:
            print("First-time")
            Nodes = list(post_order(T,T.root))
            print(len(Nodes))
            #Traverse the tree to find the ids of all the nodes
            for v in Nodes:
                #Check if it is maxima else set it as a maximum
                if T.parent(v):
                    if weight[v] <= remain and weight[T.parent(v)] > remain:
                        Q.append(v)
                        sub = v
                        #Check if it is optimal
                        if weight[v] <= remain and weight[v] + 1 > remain:
                            sub = v 
                            break
            
            Q.pop()
        else:
            print("Second-time")
            node = Q.pop()
            
            local_nodes = list(post_order(T,node))
            
            for v in local_nodes:
                if T.parent(node):
                    #Find a potential maximal subtree
                    if weight[v] <= remain and weight[T.parent(v)] > remain:
                        sub = v
                        #Check if it is optimal
                        if weight[v] <= remain and weight[v] + 1 > remain:
                            sub = v 
                            break
        
        #Change the weights based on the subtree we removed
        sub1 = np.copy(sub)
        
        for w in ancestors(T,sub):
            weight[w] -= weight[sub1]
            sub1 = w 
        #Remove the founded subtree
        sub_tree_found = list(pre_order(my_mtg,sub))
        
        if sub != T.root:
            for vtx_id in sub_tree_found:
                #Remove the vertices from the weights array and also from the tree      
                weight[vtx_id] = 0
                T.remove_tree(vtx_id)
        return sub_tree_found
        
    remain = 0
    for i in range(p):
        Qu = Priority_queue(weight,"up")
        #Initializa the queue
        target = c
        remain = target 
        first_time = True
        print("cluster",i)
        while len(C[i]) <= target:
            
            #Find and remove the founded subtree
            sub = BF(remain,first_time,Qu)
            remain = remain - len(sub)
            #if remain < 1:
            #   break
            C[i] += sub
            first_time = False

    return C




"""
#Algorithm 2
"""

#Clustering using post order traversal with priority queu
def SFC_FF(tree,p):
    vtx_id = tree.root
    C = [[] for i in range(p)]
    
    c = int(len(tree)/p)
    
    weight = np.zeros(len(tree))
    for v in post_order(tree,tree.root):
        weight[v] = 1 + sum([weight[vid] for vid in tree.children(v)])
    visited = set([])
    #Post order using a priority queue
    queue = Priority_queue(weight,"down")
    queue.append(vtx_id)
    counter = 0
    while not queue.Empty():
        vtx_id = queue.last()
        
        for vid in tree.children(vtx_id):
            if vid not in visited:
                queue.append(vid)
                break
        else: # no child or all have been visited
            counter += 1
            visited.add(vtx_id)
            queue.pop()
            C[math.ceil(counter/c)-1].append(vtx_id)
    return C

from scipy.stats import poisson, binom 

my_mtg = MTG()
dist = poisson(1., loc=1).rvs
random_tree(my_mtg,my_mtg.root, nb_children=dist,nb_vertices=99)
#my_mtg  = simple_tree(Mtg, Mtg.root,nb_children = 4, nb_vertices=100)
c = 100
#clusters = SFC_BF_DICT(my_mtg,10)
clusters1 = SFC_BF(my_mtg,c,10)
"""
print("--------------------------Algorithm 2 ------------------")
for i in range(10):

    print("------------------Cluster--------------------------",i)
    print(clusters[i])

print("-------------------------Algorithm 1 --------------------")
for i in range(10):
    
    print("-----------------Cluster---------------------------",i)
    print(clusters1[i])
"""