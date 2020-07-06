from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scoop import futures, shared
from itertools import cycle
import numpy as np 
import math
class Priority_queue:
    def __init__(self,weight,ordering="max"):
        self.heapList = [0]
        self.currentSize = 0
        self.weight = weight
        self.ordering = ordering
    
        

    def Empty(self):
        return self.currentSize == 0

    def percUp_max(self,i):
        while i // 2 > 0:
            if self.weight[self.heapList[i]] > self.weight[self.heapList[i // 2]]:
                #Swap places
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp 
            i = i // 2

    
    
    def percDown_max(self,i):
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
        
        self.percUp_max(self.currentSize)
        self.currentSize = self.currentSize + 1 
        #Place the element based on its size
        

    
    def pop(self):
        retval = self.heapList[1]
        if self.ordering == "max":
            self.heapList[1] = self.heapList[self.currentSize]
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
     
    #Compute the weights of all the nodes
    for v in post_order(T,T.root):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    #Store all the nodes inside the dictionary
    node_dict = {i:weight[i] for i in range(len(T))}
    sub = 0
    target = len(T)/p
    maxima = 0
    for i in range(p): 
        for key in node_dict:
            if T.parent(key):
                if weight[T.parent(key)] > remain and weight[v] <= remain:
                    sub = key
                    maxima = max(maxima,node_dict[key])
                if maxima + 1 > target:
                    sub = key
                    break 
        
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
    queue = Priority_queue(weight,"min")
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
            sub = queue.pop()
            
        
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
    for v in post_order(T,T.root):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    
    #Define the size of the cluster
    c = int(len(T)/p)

    def BF(remain,first_time,Q,last_cluster):
        #Add into the queue only subtrees of size that have not been added before
        sub = None
        
        if last_cluster:
            sub = T.root
        
        elif first_time:
            #Fill the queue by traversing the tree and finding the subtrees of size less than remain
            for v in post_order(T,T.root):
                #Check if it is maxima else set it as a maximum
                if T.parent(v):
                    if weight[v] <= remain and weight[T.parent(v)] > remain:
                        Q.append(v)
                        #Check if it is optimal
                        if weight[v] <= remain and weight[v] + 1 > remain:    
                            break
        

            
            if Q.size() > 0:
                sub = Q.pop()
        
        else:
        
            
            #Take a subtree from the queue and check if it has a mximal subtree
            
            max_tree = 0
            print("Queue size",Q.size())
            if Q.size() == 0:
                sub = None
            else:
                while Q.size() > 0:
                
                    node = Q.pop()
                    
                    for v in pre_order(T,node):
                        if T.parent(v):
                            #Find a potential maximal subtree
                            if weight[v] <= remain and weight[T.parent(v)] > remain and weight[v] > max_tree:
                                max_tree = weight[v]
                                sub = v
                                Q.append(v)

                            #Check if it is optimal
                            if weight[v] <= remain and weight[v] + 1 > remain:
                                break
            
        
        remove_weight = weight[sub]
        
        for w in list(ancestors(T,sub)):
            weight[w] = weight[w] - remove_weight
        #Remove the founded subtree
        
        if sub == None:
            return []

        if sub != T.root:
            sub_tree_found = list(post_order(T,sub))
            T.remove_tree(sub)
        elif sub==0:
            sub_tree_found = list(post_order(T,sub))

        return sub_tree_found
        
    remain = 0
    
    for i in range(p):
        #For each cluster initialize the queue from the begining
        Qu = Priority_queue(weight)
        
        target = c
        remain = target 
        first_time = True
        print("cluster",i)
        last_cluster = False
        while len(C[i]) <= (1 - alpha/2)*target:
            if i == p-1:
                last_cluster = True
                
            #Find and remove the founded subtree
            if remain < 1:
                break
            sub = BF(remain,first_time,Qu,last_cluster)
            if sub == []:
                break
            remain = remain - len(sub)
            
            C[i] += sub
            
            first_time = False
            
            
    return C


def cluster_1(T,p,alpha):
    #Initialize the cluster
    C = [[] for i in range(p)]
    #Initialize the remain value
    remain = 0
    #Initialize the array of weights
    weight = np.zeros(len(T))
    
    #Compute the weights for all the nodes, only once
    for v in post_order(T,T.root):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
        weight[v] = int(weight[v])
        
    
    #Define the size of the cluster
    c = int(len(T)/p)
    
    def BF(remain,first_time,Q,last_cluster):
        #Add into the queue only subtrees of size that have not been added before
        sub = None
        
        if last_cluster:
            sub = T.root
        
        elif first_time:
            #Fill the queue by traversing the tree and finding the subtrees of size less than remain
            for v in post_order(T,T.root):
                #Check if it is maxima else set it as a maximum
                if T.parent(v):
                    if weight[v] <= remain and weight[T.parent(v)] > remain:
                        
                        #Found a maximal subtree and added it to the queue
                        print("Founded subtree",weight[v])
                        Q[int(weight[v])] = v
                        
                        #Check if it is optimal
                        if weight[v] <= remain and weight[v] + 1 > remain:    
                            break
            #Enter else only if we finish the for loop without finding a best fit subtree
            index = 0
            i = len(Q) - 1
            while i > 1:
                if Q[i] != 0:
                    sub = v 
                    index = i
                    break 
                    
                i = i - 1
            #Weight of the founded subtree
            weight_sub = int(weight[v])
            #Update the queue
            i = index + 1
            while i > remain - weight_sub:
                for v in pre_order(T,Q[i]):
                     if T.parent(v):
                        if weight[v] <= remain-weight_sub and weight[T.parent(v)] > remain-weight_sub:
                            Q[weight[v]] = sub
                Q[i] = 0
                i = i-1
            remain = remain - weight_sub

        else:
            index = 0
            i = remain
            while i > 1:
                if Q[i] != 0:
                    sub = v 
                    index = i
                    break 

                i = i - 1
            #Weight of the founded subtree
            weight_sub = weight[sub]
            #Update the queue
            for i in range(remain - weight_sub,index+1):
                if i > 0:
                    print("node index",Q[i])
                    for v in preorder_order(T,Q[i]):
                        if T.parent(v):
                            if weight[v] <= remain - weight_sub and weight[T.parent(v)] > remain - weight_sub:
                                Q[weight[v]] = v
                    Q[i] = 0    
            remain = remain - weight_sub 
        remove_weight = weight_sub
        
        for w in list(ancestors(T,sub)):
            weight[w] = int(weight[w] - remove_weight)
        #Remove the founded subtree

        if sub != T.root:
            sub_tree_found = list(post_order(T,sub))
            T.remove_tree(sub)
        elif sub==0:
            sub_tree_found = list(post_order(T,sub))

        return sub_tree_found
        
    remain = 0
    
    for i in range(p):
        #For each cluster initialize the queue from the begining
        
        
        target = c + remain
        remain = target 
        first_time = True
        print("cluster",i)
        last_cluster = False
        Qu = [0 for i in range(remain+1)]
        while len(C[i]) <= (1 - alpha/2)*target:
            if i == p-1:
                last_cluster = True
            #Fills the queue if first time and searches for subtree if second time
            sub = BF(remain,first_time,Qu,last_cluster)
            
            C[i] += sub
            first_time = False

    return C







from scipy.stats import poisson, binom 

my_mtg = MTG()
my_mtg1 = MTG()
dist = poisson(1., loc=1).rvs
random_tree(my_mtg,my_mtg.root, nb_children=3,nb_vertices=99)
random_tree(my_mtg1,my_mtg1.root, nb_children=dist,nb_vertices=99)

#my_mtg  = simple_tree(Mtg, Mtg.root,nb_children = 4, nb_vertices=100)

clusters = cluster_1(my_mtg,10,0)
#clusters1 = SFC_FF(my_mtg1,10)

for i in range(10):
    #print("---------------------------Cluster---------------",i)
    #print("Cluster",i,"for SFC_FF")
    #print(clusters1[i])
    print("Cluster",i,"for SFC_BF")
    print(clusters[i])
