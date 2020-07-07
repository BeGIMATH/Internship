from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scoop import futures, shared
from itertools import cycle
import numpy as np 
import math
import os
import timeit
import sys

class Priority_queue:
    def __init__(self,weights):
        self.heapList = [0]
        self.currentSize = 0
        self.weights = weights
        

    def Empty(self):
        return self.currentSize == 0

    def percUp(self,i):
        while i // 2 > 0:
          if self.weights[self.heapList[i]] > self.weights[self.heapList[i // 2]]:
             tmp = self.heapList[i // 2]
             self.heapList[i // 2] = self.heapList[i]
             self.heapList[i] = tmp
          i = i // 2

    def append(self,k):
      self.heapList.append(k)
      self.currentSize = self.currentSize + 1
      self.percUp(self.currentSize)

    def percDown(self,i):
      while (i * 2) <= self.currentSize:
          mc = self.maxChild(i)
          if self.weights[self.heapList[i]] < self.weights[self.heapList[mc]]:
              tmp = self.heapList[i]
              self.heapList[i] = self.heapList[mc]
              self.heapList[mc] = tmp
          i = mc

    def maxChild(self,i):
      if i * 2 + 1 > self.currentSize:
          return i * 2
      else:
          if self.weights[self.heapList[i*2]] > self.weights[self.heapList[i*2+1]]:
              return i * 2
          else:
              return i * 2 + 1

    def pop(self):
      retval = self.heapList[1]
      self.heapList[1] = self.heapList[self.currentSize]
      self.currentSize = self.currentSize - 1
      self.heapList.pop()
      self.percDown(1)
      return retval

      
    def size(self):
      return self.currentSize
    
    def last(self):
        return self.heapList[1]
    
    def buildHeap(self,alist):
      i = len(alist) // 2
      self.currentSize = len(alist)
      self.heapList = [0] + alist[:]
      while (i > 0):
          self.percDown(i)
          i = i - 1

"""
#Algorithm 1
"""
### To be done ###


import pdb as pd


#Single fill
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
            #pd.set_trace()
            #Fill the queue by traversing the tree and finding the subtrees of size less than remain
            for v in post_order(T,T.root):
                #Check if it is maxima else set it as a maximum
                if T.parent(v):
                    if weight[v] <= remain and weight[T.parent(v)] > remain:
                        Q.append(v)
                        #Check if it is optimal
                        if weight[v] <= remain and weight[v] + 1 > remain:
                            break
            else:
                print("No perfect subtree found")
           
            sub = Q.pop()
           
            
            index = weight[sub]
           
            #Problem localized
            print(index)
            if remain - index > 0:
                while weight[Q.last()] > remain - index:
                    node = Q.pop()
                    for v in pre_order(T,node):
                        if T.parent(v):
                            if weight[v] <= remain - index and weight[T.parent(v)] > remain - index:
                                Q.append(v)
                               
               
            
            for w in list(ancestors(T,sub)):
                weight[w] = weight[w] - index
        else:
        
           
            
            sub = Q.pop()
            index = weight[sub]
            
            if remain - index > 0:
                while weight[Q.last()] > remain - index:
                    node = Q.pop()   
                    for v in pre_order(T,node):
                        if T.parent(v):
                            #Find a potential maximal subtree
                            if weight[v] <= remain - index and weight[T.parent(v)] > remain - index:
                                Q.append(v)

                     

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
        last_cluster = False
        while len(C[i]) <= (1 - alpha/2)*target:
            if i == p-1:
                last_cluster = True
            if remain < 1:
                break    
            
            sub = BF(remain,first_time,Qu,last_cluster)
            
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
    weight = weight.astype(int)
    
    #Compute the weights for all the nodes, only once
    for v in post_order(T,T.root):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    
        
    
    #Define the size of the cluster
    c = int(len(T)/p)
    
    def BF(remain,first_time,Q,last_cluster):
        #Add into the queue only subtrees of size that have not been added before
        sub = None
        index = 0
        if last_cluster:
            sub = T.root
        
        elif first_time:
            
            
            #Fill the queue by traversing the tree and finding the subtrees of size less than remain
            for v in post_order(T,T.root):
                #Check if it is maxima else set it as a maximum
                if T.parent(v):
                    if weight[v] <= remain and weight[T.parent(v)] > remain:
                        #Found a maximal subtree and added it to the queue
                        if Q[weight[v]] == None:
                            Q[weight[v]] = v
                        #Check if it is optimal
                        if weight[v] <= remain and weight[v] + 1 > remain:    
                            break
            #Enter else only if we finish the for loop without finding a best fit subtree
            
            i = len(Q) - 1
            while i > 1:
                if Q[i] != None:
                    index = i
                    sub = Q[index]
                    Q[i] = None
                    break 
                i = i - 1
            
            
            #Update the queue
            
            i = index - 1
            if remain - index > 0:
                while i > remain - index:
                    for v in pre_order(T,Q[i]):
                        if T.parent(v):
                            if weight[v] < remain -index and weight[T.parent(v)] > remain - index:
                                Q[weight[v]] = v
                                
                    Q[i] = None
                    i = i-1
            
            
            remove_weight = index
        
            for w in list(ancestors(T,sub)):
                weight[w] = weight[w] - remove_weight
           
        else:
            i = remain
            while i > 0:
                if Q[i] != None:
                    index = i
                    sub = Q[i] 
                    Q[i] = None
                    break 

                i = i - 1
            #Weight of the founded subtree
            
            #Update the queue
            i = index
            if remain - index > 0:
                while i > remain - index:
                    for v in pre_order(T,Q[i]):
                        if T.parent(v):
                            if weight[v] < remain - index and weight[T.parent(v)] > remain - index:
                                Q[weight[v]] = v
                    Q[i] = None
                    i = i - 1    
    
            remove_weight = index
          
            for w in list(ancestors(T,sub)):
                weight[w] = weight[w] - remove_weight
        #Remove the founded subtree

        if sub != T.root:
            sub_tree_found = list(post_order(T,sub))
            T.remove_tree(sub)
        elif sub == T.root:
            sub_tree_found = list(post_order(T,sub))
        return sub_tree_found
        
    remain = 0
    
    for i in range(p):
        #For each cluster initialize the queue from the begining
        
        
        target = c
        remain = target
        first_time = True
        last_cluster = False
        Qu = [None for i in range(remain+1)]
        while len(C[i]) < (1 - alpha/2)*target:
            if i == p-1:
                last_cluster = True
            
            #Fills the queue if first time and searches for subtree if second time
            sub = BF(remain,first_time,Qu,last_cluster)
            if sub == None:
                break
            remain = remain - len(sub)
            C[i] += sub
            first_time = False
    return C

def SFC_FF(tree,p):
    vtx_id = tree.root
    C = [[] for i in range(p)]
    weight = np.zeros(len(tree))
    visited = set([])
    def order_children(vid):
        ordered = []
        #Sort the children of a node using the priority queue
        p_queue = Priority_queue(weight)
        for vid in tree.children(vid):
            p_queue.append(vid)
        while p_queue.size() > 0:
            node = p_queue.pop()
            ordered.append(node)
        return ordered

    for v in post_order(tree,tree.root):
        weight[v] = 1 + sum([weight[vid] for vid in tree.children(v)])
    
    c = int(len(tree)/p)
    
    
    queue = [vtx_id]
    
    counter = 0
    while queue:
        vtx_id = queue[-1]
        for vid in order_children(vtx_id):
            if vid not in visited:
                queue.append(vid)
                break
        else: # no child or all have been visited
            counter += 1
            #print("Counter",counter)
            visited.add(vtx_id)
            #print(math.ceil(counter/c)-1)
            C[math.ceil(counter/c)-1].append(vtx_id)
            queue.pop()
    return C



def SFC_FF_1(tree,p):
    vtx_id = tree.root
    C = [[] for i in range(p)]
    weight = np.zeros(len(tree))
    visited = set([])
    def order_children(vid):
        ordered = []
        #Sort the children of a node using the priority queue
        p_queue = Priority_queue(weight)
        for vid in tree.children(vid):
            ordered.append(vid)
        p_queue.buildHeap(ordered)
        
        return ordered

    for v in post_order(tree,tree.root):
        weight[v] = 1 + sum([weight[vid] for vid in tree.children(v)])
    
    c = int(len(tree)/p)
    
    
    queue = [vtx_id]
    
    counter = 0
    while queue:
        vtx_id = queue[-1]
        for vid in order_children(vtx_id):
            if vid not in visited:
                queue.append(vid)
                break
        else: # no child or all have been visited
            counter += 1
            #print("Counter",counter)
            visited.add(vtx_id)
            #print(math.ceil(counter/c)-1)
            C[math.ceil(counter/c)-1].append(vtx_id)
            queue.pop()
    return C