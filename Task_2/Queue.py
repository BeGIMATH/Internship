from openalea.mtg.mtg import *
from openalea.mtg.algo import ancestors
from openalea.mtg.io import *
from openalea.mtg.traversal import *
from scoop import futures, shared
from itertools import cycle
import numpy as np 
import math

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

def SFC_BF(T,p,alpha):
    
    C = [[] for i in range(p)]
    
    remain = 0
    
    weight = np.zeros(len(T))
    
    for v in post_order(T,T.root):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    
    c = int(len(T)/p)

    def BF(remain,first_time,Q,last_cluster):
        
        sub = None
        
        if last_cluster:
            sub = T.root
        
        elif first_time:
            for v in post_order(T,T.root):
                
                if T.parent(v) != None:
                    if weight[v] <= remain and weight[T.parent(v)] > remain:
                        Q.append(v)
                        if weight[v] + 1 > remain:
                            break
               
            if Q.size() > -1:
                sub = Q.pop()

                index = weight[sub]
           
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
                            if weight[v] <= remain - index and weight[T.parent(v)] > remain - index:
                                Q.append(v)

                     

            remove_weight = weight[sub]
        
            for w in list(ancestors(T,sub)):
                weight[w] = weight[w] - remove_weight
       
        
        
        if sub != T.root:
            sub_tree_found = list(post_order(T,sub))
            T.remove_tree(sub)
        elif sub==0:
            sub_tree_found = list(post_order(T,sub))
        elif sub == None:
            sub_tree_found = []
        return sub_tree_found
        
    remain = 0
    
    for i in range(p):
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

def SFC_BF_PAPER(T,p,alpha):
    
    C = [[] for i in range(p)]
    
    remain = 0
    
    weight = np.zeros(len(T))
    weight = weight.astype(int)
    
    
    for v in post_order(T,T.root):
        weight[v] = 1 + sum([weight[vid] for vid in T.children(v)])
    
        
    
    c = int(len(T)/p)
    
    def BF(remain,first_time,Q,last_cluster):
       
        sub = None
        index = 0
        if last_cluster:
            sub = T.root
        
        elif first_time:
            for v in post_order(T,T.root):
                if T.parent(v) != None:
                    if weight[v] <= remain and weight[T.parent(v)] > remain:
                        if Q[weight[v]] == None:
                            Q[weight[v]] = v
                        if weight[v] <= remain and weight[v] + 1 > remain:    
                            break

            i = len(Q) - 1
            while i > 1:
                if Q[i] != None:
                    index = i
                    sub = Q[index]
                    Q[i] = None
                    break 
                i = i - 1
            
            i = index - 1
            if remain - index > 0:
                while i > remain - index:
                    for v in pre_order(T,Q[i]):
                        if T.parent(v) != None:
                            if weight[v] <= remain -index and weight[T.parent(v)] > remain - index:
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
            
            i = index
            if remain - index > 0:
                while i > remain - index:
                    for v in pre_order(T,Q[i]):
                        if T.parent(v) != None:
                            if weight[v] <= remain - index and weight[T.parent(v)] > remain - index:
                                Q[weight[v]] = v
                    Q[i] = None
                    i = i - 1    
    
            remove_weight = index
          
            for w in list(ancestors(T,sub)):
                weight[w] = weight[w] - remove_weight
       

        if sub != T.root:
            sub_tree_found = list(post_order(T,sub))
            T.remove_tree(sub)
        elif sub == T.root:
            sub_tree_found = list(post_order(T,sub))
        return sub_tree_found
        
    remain = 0
    
    for i in range(p):
        target = c
        remain = target
        first_time = True
        last_cluster = False
        Qu = [None for i in range(remain+1)]
        while len(C[i]) < (1 - alpha/2)*target:
            if i == p-1:
                last_cluster = True
            
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
        else: 
            counter += 1
            visited.add(vtx_id)
            C[math.ceil(counter/c)-1].append(vtx_id)
            queue.pop()
    return C


