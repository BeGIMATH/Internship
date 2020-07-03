from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
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
        

    def Empty(self):
        return self.currentSize == 0

    def percUp(self,i):
        while i // 2 > 0:
            if self.weight[self.heapList[i]] > self.weight[self.heapList[i // 2]]:
                #Swap places
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp 
            i = i // 2
    
    def percDown(self,i):
      while (i * 2) <= self.currentSize:
          mc = self.maxChild(i)
          if self.weight[self.heapList[i]] < self.weight[self.heapList[mc]]:
              tmp = self.heapList[i]
              self.heapList[i] = self.heapList[mc]
              self.heapList[mc] = tmp
          i = mc

    def maxChild(self,i):
      if i * 2 + 1 > self.currentSize:
          return i * 2
      else:
          if self.heapList[i*2] > self.heapList[i*2+1]:
              return i * 2
          else:
              return i * 2 + 1

    
    
    def append(self,x):
        #Insert the element at the end of the list 
        self.heapList.append(x)
        #Increment the size variable
        self.percUp(self.currentSize)
        self.currentSize = self.currentSize + 1 
        #Place the element based on its size
        

    
    def pop(self):
      retval = self.heapList[1]
      self.heapList[1] = self.heapList[self.currentSize]
      self.currentSize = self.currentSize - 1
      self.heapList.pop()
      self.percDown(1)
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



def SFC_BF(T,p,alpha):
    #Initialize the cluster
    C = [[] for i in range(p)]
    #Initialize the remain value
    remain = 0
    #Initialize the array of weights
    weight = np.zeros(len(T))
    
    #Compute the weights for all the nodes, only once
    for v in list(post_order(T,T.root)):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    
    #Define the size of the cluster
    c = int(len(T)/p)

    def BF(remain,first_time,Q):
        #Add into the queue only subtrees of size that have not been added before
        sub = None
        
        if first_time:
            print("First-time")
            
            Nodes = list(post_order(T,T.root))

            print("Nodes left inside the tree", len(Nodes))
            #Fill the queue by traversing the tree and finding the subtrees of size less than remain
            for v in Nodes:
                #Check if it is maxima else set it as a maximum
                if T.parent(v):
                    if weight[v] <= remain and weight[T.parent(v)] > remain:
                        Q.append(v)
                        print("Weight of the subtree added",weight[v])
                        
                        #Check if it is optimal
                        if weight[v] <= remain and weight[v] + 1 > remain:
                            print("Found optimal subtree")
                            Q.append(v) 
                            break
            if len(Nodes) <= c:
                sub = 0   
            if Q.size() > 0:
                sub = Q.pop()
        else:
            print("Second-time")
            
            #Take a subtree from the queue and check if it has a mximal subtree
            sub_tree_not_found = True 
            sub_tree_size = 0
            while sub_tree_not_found and Q.size() > 0:
                
                node = Q.pop()
            
                local_nodes = list(post_order(T,node))
            
                for v in local_nodes:
                    if T.parent(v):
                        #Find a potential maximal subtree
                        if weight[v] <= remain and weight[T.parent(v)] > remain and weight[v] > sub_tree_size:
                            sub_tree_size = weight[v]
                            sub = v
                        
                        #Check if it is optimal
                        if weight[v] <= remain and weight[v] + 1 > remain:
                            sub = v 
                            sub_tree_not_found = False
                            
            
        remove_weight = weight[sub]
        
        for w in list(ancestors(T,sub)):
            weight[w] = weight[w] - remove_weight
        #Remove the founded subtree
        sub_tree_found = list(pre_order(my_mtg,sub))
        print("Length of the founded subtree",len(sub_tree_found))
        if sub != T.root:
            for vtx_id in sub_tree_found:
                #Remove the vertices from the weights array and also from the tree      
                T.remove_tree(vtx_id)
        return sub_tree_found
        
    remain = 0
    
    for i in range(p):
        #For each cluster initializa the queue from the begining
        Qu = Priority_queue(weight)
       
        target = c
        remain = target 
        first_time = True
        print("cluster",i)
        
        while len(C[i]) <= (1 - alpha/2)*target:
            
            #Find and remove the founded subtree
            
            sub = BF(remain,first_time,Qu)
            
            remain = remain - len(sub)
            
            C[i] += sub
            
            first_time = False

    return C






from scipy.stats import poisson, binom 

my_mtg = MTG()
dist = poisson(1., loc=1).rvs
random_tree(my_mtg,my_mtg.root, nb_children=dist,nb_vertices=99)
#my_mtg  = simple_tree(Mtg, Mtg.root,nb_children = 4, nb_vertices=100)

clusters = SFC_BF(my_mtg,10,0.1)
#clusters1 = SFC_FF(my_mtg,10)

for i in range(10):
    print("---------------------------Cluster---------------",i)
    print(clusters[i])
"""

A = list(post_order(my_mtg,my_mtg.root))

weight = np.zeros(len(my_mtg))
Q = Priority_queue(weight)
#Compute the weights for all the nodes, only once
for v in list(post_order(my_mtg,my_mtg.root)):
    weight[v] = 1 + sum([weight[vid] for vid in my_mtg.children(v)])

for i in range(20):
    print(A[i],weight[A[i]])
    Q.append(A[i])

while Q.size() > 0:
    print(Q.pop())

"""